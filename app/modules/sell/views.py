from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Transaction, Customer, Warehouse, Company
from app.modules.sell.forms import SellForm
from app.modules.detail.forms import DetailForm
from app.functions import to
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardSell(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif (key == 'customer') | (key == 'warehousein'):
                filters[key] = value
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Sell'
    datasPrev = Transaction.objects.filter(**filters).annotate(
        total= Sum(F('details__qty')* F('details__price_sell')*-1)
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
    customers = Customer.objects.filter()
    warehouses = Warehouse.objects.filter()
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('sell/','sell/print/')
    context = {
        'print_url': print_url,
        'customers': customers,
        'warehouses': warehouses,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }    
    request.session['menu'] = 'dashboard-sell'
    return render(request, 'sell/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardSellCreate(request):
    form = SellForm()
    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.kind = 'Sell'
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-sell'
            return redirect('dashboard-sell-edit', form.id)
    context = {'form': form, 'status': 'create'}
    request.session['menu'] = 'dashboard-sell'
    return render(request, 'sell/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardSellEdit(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    form = SellForm(instance=data)
    detailForm = DetailForm(initial={'transaction': data.id})
    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-sell'
            return redirect('dashboard-sell')
    context = {'form': form, 'details': details, 'detailForm': detailForm, 'status': 'edit'}
    request.session['menu'] = 'dashboard-sell'
    return render(request, 'sell/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardSellInvoice(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    total_sell = 0
    for detail in details:
        total_sell += (detail.qty*detail.price_sell)*-1
    company = Company.objects.first()
    context = {
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'data': data,
        'details': details,
        'total_sell': to.rupiah('{:.2f}'.format(total_sell))
    }
    return to.pdf(request,'sell/templates/invoice.html',context)

@login_required(login_url='/login/')
def dashboardSellPrint(request):
    customer = ''
    warehousein = ''
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif key == 'customer':
                filters[key] = value
                customer = Customer.objects.get(id=value)
                customer = customer.name
            elif key == 'warehousein':
                filters[key] = value
                warehousein = Warehouse.objects.get(id=value)
                warehousein = warehousein.name
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Sell'
    datasPrev = Transaction.objects.filter(**filters).annotate(
        total= Sum(F('details__qty')* F('details__price_sell')*-1)
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
        'customer': customer,
        'warehousein': warehousein,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }    
    return to.pdf(request,'sell/templates/print.html',context)

@login_required(login_url='/login/')
def dashboardSellDelete(request, id):
    data = Transaction.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-sell'
    return redirect('dashboard-sell')