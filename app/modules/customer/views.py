from datetime import datetime
from django.db import reset_queries
from django.shortcuts import render, redirect

from app.models import Customer, Company
from app.modules.customer.forms import CustomerForm
import uuid
from django.contrib import messages
from django.db.models import OuterRef, Subquery, Q
from app.functions import to
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardCustomer(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Customer.objects.filter(**filters)
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('customer/','customer/print/')
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'print_url': print_url,
        'datas': datas,
        'filters': filters
    }
    request.session['menu'] = 'dashboard-customer'
    return render(request, 'customer/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardCustomerCreate(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-customer'
            return redirect('dashboard-customer')
    context = {'form': form}
    request.session['menu'] = 'dashboard-customer'
    return render(request, 'customer/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardCustomerEdit(request, id):
    data = Customer.objects.get(id=id)
    form = CustomerForm(instance=data)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-customer'
            return redirect('dashboard-customer')
    context = {'form': form}
    request.session['menu'] = 'dashboard-customer'
    return render(request, 'customer/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardCustomerDelete(request, id):
    data = Customer.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-customer'
    return redirect('dashboard-customer')

@login_required(login_url='/login/')
def dashboardCustomerPrint(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Customer.objects.filter(**filters)
    company = Company.objects.first()
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'datas': datas,
        'filters': filters
    }
    return to.pdf(request,'customer/templates/print.html',context)
