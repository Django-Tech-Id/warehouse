from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Transaction, Warehouse, Company
from app.modules.moveout.forms import MoveoutForm
from app.modules.movein.forms import MoveinForm
from app.modules.detail.forms import DetailForm
from app.functions import to
from django.db.models import F, Sum
from django.contrib import messages

# Create your views here.
def dashboardMoveout(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif (key == 'warehousein'):
                filters['warehouseout'] = value
            elif (key == 'warehouseout'):
                filters['warehousein'] = value
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Move Out'
    datasPrev = Transaction.objects.filter(**filters).annotate(
        total= Sum(F('details__qty')* F('details__price'))*-1
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
    print_url = print_url.replace('moveout/','moveout/print/')
    context = {
        'print_url': print_url,
        'warehouses': warehouses,
        'datas': datas,
        'filters': filters,
        'operator': operatorSign,
        'total': total,
        'filterOperators': filterOperators
    }
    request.session['menu'] = 'dashboard-moveout'
    return render(request, 'moveout/templates/index.html', context)

def dashboardMoveoutCreate(request):
    form = MoveoutForm()
    if request.method == 'POST':
        form = MoveoutForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.kind = 'Move Out'
            form.created_by = request.user
            form.save()

            formMovein = MoveinForm(request.POST, request.FILES)
            formMovein = formMovein.save(commit=False)

            #BUAT TRANSAKSI MOVE IN
            formMovein.transaction = form
            formMovein.kind = 'Move In'
            formMovein.warehousein = form.warehouseout
            formMovein.warehouseout = form.warehousein
            formMovein.code = request.POST['code'] #MANIPULASI KODE OTOMATIS
            formMovein.status = 'Created'
            formMovein.created_by = request.user
            formMovein.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-moveout'
            return redirect('dashboard-moveout-edit', form.id)
    context = {'form': form, 'status': 'create'}
    request.session['menu'] = 'dashboard-moveout'
    return render(request, 'moveout/templates/form.html', context)

def dashboardMoveoutEdit(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    form = MoveoutForm(instance=data)
    detailForm = DetailForm(initial={'transaction': data.id})
    if request.method == 'POST':
        form = MoveoutForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-moveout'
            return redirect('dashboard-moveout')
    context = {'form': form, 'details': details, 'detailForm': detailForm, 'status': 'edit'}
    request.session['menu'] = 'dashboard-moveout'
    return render(request, 'moveout/templates/form.html', context)

def dashboardMoveoutInvoice(request, id):
    data = Transaction.objects.get(id=id)
    details = data.details.all()
    total = 0
    for detail in details:
        total += (detail.qty*detail.price)*-1
    company = Company.objects.first()
    context = {
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'data': data,
        'details': details,
        'total': to.rupiah('{:.2f}'.format(total))
    }
    return to.pdf(request,'moveout/templates/invoice.html',context)

def dashboardMoveoutPrint(request):
    warehousein = ''
    warehouseout = ''
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'start_date':
                filters['date__gte'] = value
            elif key == 'end_date':
                filters['date__lte'] = value
            elif (key == 'warehousein'):
                filters['warehouseout'] = value
                warehousein = Warehouse.objects.get(id=value)
                warehousein = warehousein.name
            elif (key == 'warehouseout'):
                filters['warehousein'] = value
                warehouseout = Warehouse.objects.get(id=value)
                warehouseout = warehouseout.name
            elif (key == 'operator') | (key == 'total'):
                continue
            else:
                filters[key+'__icontains'] = value
    filters['kind'] = 'Move Out'
    datasPrev = Transaction.objects.filter(**filters).annotate(
        total= Sum(F('details__qty')* F('details__price'))*-1
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
    return to.pdf(request,'moveout/templates/print.html',context)

def dashboardMoveoutDelete(request, id):
    data = Transaction.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-moveout'
    return redirect('dashboard-moveout')
