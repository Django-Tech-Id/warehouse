from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Company, Supplier, Transaction, Warehouse
from app.modules.buy.forms import BuyForm
from app.modules.detail.forms import DetailForm
from app.functions import to
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardBuy(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif (key == 'supplier') | (key == 'warehousein'):
                filters[key] = value
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Buy'
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
    suppliers = Supplier.objects.filter()
    warehouses = Warehouse.objects.filter()
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('buy/','buy/print/')
    context = {
        'print_url': print_url,
        'suppliers': suppliers,
        'warehouses': warehouses,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }
    request.session['menu'] = 'dashboard-buy'
    return render(request, 'buy/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardBuyCreate(request):
    form = BuyForm()
    if request.method == 'POST':
        form = BuyForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.kind = 'Buy'
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-buy'
            return redirect('dashboard-buy-edit',form.id)
    context = {'form': form, 'status': 'create'}
    request.session['menu'] = 'dashboard-buy'
    return render(request, 'buy/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardBuyEdit(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    form = BuyForm(instance=data)
    detailForm = DetailForm(initial={'transaction': data.id})
    if request.method == 'POST':
        form = BuyForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-buy'
            return redirect('dashboard-buy')
    context = {'form': form, 'details': details, 'detailForm': detailForm, 'status': 'edit'}
    request.session['menu'] = 'dashboard-buy'
    return render(request, 'buy/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardBuyInvoice(request, id):
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
    return to.pdf(request,'buy/templates/invoice.html',context)

@login_required(login_url='/login/')
def dashboardBuyPrint(request):
    supplier = ''
    warehousein = ''
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif key == 'supplier':
                filters[key] = value
                supplier = Supplier.objects.get(id=value)
                supplier = supplier.name
            elif key == 'warehousein':
                filters[key] = value
                warehousein = Warehouse.objects.get(id=value)
                warehousein = warehousein.name
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Buy'
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
        'supplier': supplier,
        'warehousein': warehousein,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }
    return to.pdf(request,'buy/templates/print.html',context)

@login_required(login_url='/login/')
def dashboardBuyDelete(request, id):
    data = Transaction.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-buy'
    return redirect('dashboard-buy')