from datetime import datetime
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect

from app.models import Detail, Transaction, Warehouse, Company
from app.modules.movein.forms import MoveinForm
from app.modules.detail.forms import DetailForm
from app.functions import to
from django.db.models import F, Sum
from django.core import serializers
from django.http import JsonResponse
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardMovein(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif key == 'start_pending_date':
                filters['pending_date__gte'] = value
            elif key == 'end_pending_date':
                filters['pending_date__lte'] = value
            elif key == 'start_accepted_date':
                filters['accepted_date__gte'] = value
            elif key == 'end_accepted_date':
                filters['accepted_date__lte'] = value
            elif (key == 'warehousein') | (key == 'warehouseout'):
                filters[key] = value
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Move In'
    print(filters)
    datasPrev = Transaction.objects.filter(**filters).annotate(
        total= Sum(F('details__qty')* F('details__price'))
    )
    operator = ''
    operatorSign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operator':
                if value == 'e':
                    operator = ''
                    operatorSign = 'e'
                elif value == 'lt':
                    operator = '__lt'
                    operatorSign = 'lt'
                elif value == 'lte':
                    operator = '__lte'
                    operatorSign = 'lte'
                elif value == 'gt':
                    operator = '__gt'
                    operatorSign = 'gt'
                elif value == 'gte':
                    operator = '__gte'
                    operatorSign = 'gte'
    filterOperators = {}
    total = ''
    if 'total' in request.GET:
        if request.GET['total'] != '':
            filterOperators['total'+operator] = request.GET['total']
            total = request.GET['total']
    datas = datasPrev.filter(**filterOperators)
    warehouses = Warehouse.objects.filter()
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('movein/','movein/print/')
    context = {
        'print_url': print_url,
        'warehouses': warehouses,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }
    request.session['menu'] = 'dashboard-movein'
    return render(request, 'movein/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardMoveinEdit(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    form = MoveinForm(instance=data)
    detailForm = DetailForm(initial={'transaction': data.id})
    if request.method == 'POST':
        form = MoveinForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.status = request.POST['status']
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            return redirect('dashboard-movein')
    context = {'form': form, 'details': details, 'detailForm': detailForm, 'status': 'edit'}
    request.session['menu'] = 'dashboard-movein'
    return render(request, 'movein/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardMoveinInvoice(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    total = 0
    for detail in details:
        total += (detail.qty*detail.price)
    company = Company.objects.first()
    context = {
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'data': data,
        'details': details,
        'total': to.rupiah('{:.2f}'.format(total))
    }
    return to.pdf(request,'movein/templates/invoice.html',context)

@login_required(login_url='/login/')
def dashboardMoveinPrint(request):
    warehousein = ''
    warehouseout = ''
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif key == 'start_pending_date':
                filters['pending_date__gte'] = value
            elif key == 'end_pending_date':
                filters['pending_date__lte'] = value
            elif key == 'start_accepted_date':
                filters['accepted_date__gte'] = value
            elif key == 'end_accepted_date':
                filters['accepted_date__lte'] = value
            elif key == 'warehousein':
                filters[key] = value
                warehousein = Warehouse.objects.get(id=value)
                warehousein = warehousein.name
            elif key == 'warehouseout':
                filters[key] = value
                warehouseout = Warehouse.objects.get(id=value)
                warehouseout = warehouseout.name
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Move In'
    datasPrev = Transaction.objects.filter(**filters).annotate(
        total= Sum(F('details__qty')* F('details__price'))
    )
    operator = ''
    operatorSign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operator':
                if value == 'e':
                    operator = ''
                    operatorSign = 'e'
                elif value == 'lt':
                    operator = '__lt'
                    operatorSign = 'lt'
                elif value == 'lte':
                    operator = '__lte'
                    operatorSign = 'lte'
                elif value == 'gt':
                    operator = '__gt'
                    operatorSign = 'gt'
                elif value == 'gte':
                    operator = '__gte'
                    operatorSign = 'gte'
    filterOperators = {}
    total = ''
    if 'total' in request.GET:
        if request.GET['total'] != '':
            filterOperators['total'+operator] = request.GET['total']
            total = request.GET['total']
    datas = datasPrev.filter(**filterOperators)
    company = Company.objects.first()
    context = {
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'warehousein': warehousein,
        'warehouseout': warehouseout,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }
    return to.pdf(request,'movein/templates/print.html',context)