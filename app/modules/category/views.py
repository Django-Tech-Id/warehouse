from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Category, Company
from app.modules.category.forms import CategoryForm
import uuid
from django.contrib import messages
from app.functions import to

# Create your views here.
def dashboardCategory(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Category.objects.filter(**filters)
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('category/','category/print/')
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'print_url': print_url,
        'datas': datas,
        'filters': filters
    }
    request.session['menu'] = 'dashboard-category'
    return render(request, 'category/templates/index.html', context)

def dashboardCategoryCreate(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-category'
            return redirect('dashboard-category')
    context = {'form': form}
    request.session['menu'] = 'dashboard-category'
    return render(request, 'category/templates/form.html', context)

def dashboardCategoryEdit(request, id):
    data = Category.objects.get(id=id)
    form = CategoryForm(instance=data)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-category'
            return redirect('dashboard-category')
    context = {'form': form}
    request.session['menu'] = 'dashboard-category'
    return render(request, 'category/templates/form.html', context)

def dashboardCategoryDelete(request, id):
    data = Category.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-category'
    return redirect('dashboard-category')

def dashboardCategoryPrint(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            filters[key+'__icontains'] = value    
    datas = Category.objects.filter(**filters)
    company = Company.objects.first()
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'image_path': image_path,
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'datas': datas,
        'filters': filters
    }
    return to.pdf(request,'category/templates/print.html',context)
