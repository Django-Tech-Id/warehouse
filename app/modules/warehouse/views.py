from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Warehouse, Company
from app.modules.warehouse.forms import WarehouseForm
import uuid
from django.contrib import messages
from app.functions import to
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardWarehouse(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Warehouse.objects.filter(**filters)
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('warehouse/','warehouse/print/')
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'print_url': print_url,
        'datas': datas,
        'filters': filters
    }
    request.session['menu'] = 'dashboard-warehouse'
    return render(request, 'warehouse/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardWarehouseCreate(request):
    form = WarehouseForm()
    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-warehouse'
            return redirect('dashboard-warehouse')
    context = {'form': form}
    request.session['menu'] = 'dashboard-warehouse'
    return render(request, 'warehouse/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardWarehouseEdit(request, id):
    data = Warehouse.objects.get(id=id)
    form = WarehouseForm(instance=data)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-warehouse'
            return redirect('dashboard-warehouse')
    context = {'form': form}
    request.session['menu'] = 'dashboard-warehouse'
    return render(request, 'warehouse/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardWarehouseDelete(request, id):
    data = Warehouse.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-warehouse'
    return redirect('dashboard-warehouse')

@login_required(login_url='/login/')
def dashboardWarehousePrint(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Warehouse.objects.filter(**filters)
    company = Company.objects.first()
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'datas': datas,
        'filters': filters
    }
    return to.pdf(request,'warehouse/templates/print.html',context)
