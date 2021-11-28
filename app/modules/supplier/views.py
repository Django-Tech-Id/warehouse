from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Supplier, Company
from app.modules.supplier.forms import SupplierForm
import uuid
from django.contrib import messages
from app.functions import to

# Create your views here.
def dashboardSupplier(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Supplier.objects.filter(**filters)
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('supplier/','supplier/print/')
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'print_url': print_url,
        'datas': datas,
        'filters': filters
    }
    request.session['menu'] = 'dashboard-supplier'
    return render(request, 'supplier/templates/index.html', context)

def dashboardSupplierCreate(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-supplier'
            return redirect('dashboard-supplier')
    context = {'form': form}
    request.session['menu'] = 'dashboard-supplier'
    return render(request, 'supplier/templates/form.html', context)

def dashboardSupplierEdit(request, id):
    data = Supplier.objects.get(id=id)
    form = SupplierForm(instance=data)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-supplier'
            return redirect('dashboard-supplier')
    context = {'form': form}
    request.session['menu'] = 'dashboard-supplier'
    return render(request, 'supplier/templates/form.html', context)

def dashboardSupplierDelete(request, id):
    data = Supplier.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-supplier'
    return redirect('dashboard-supplier')

def dashboardSupplierPrint(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Supplier.objects.filter(**filters)
    company = Company.objects.first()
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'datas': datas,
        'filters': filters
    }
    return to.pdf(request,'supplier/templates/print.html',context)
