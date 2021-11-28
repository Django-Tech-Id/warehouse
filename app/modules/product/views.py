from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Category, Product, Supplier, Company
from app.modules.product.forms import ProductForm
import uuid
from django.contrib import messages
from app.functions import to, validate
from django.db.models import F, Sum
from django.db.models import OuterRef, Subquery, Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardProduct(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if (key == 'category') | (key == 'supplier'):
                filters[key] = value   
            elif (key == 'operatorbuy') | (key == 'buy_price') | (key == 'operatorsell') | (key == 'sell_price') | (key == 'operatormargin') | (key == 'margin'):
                continue
            else:
                filters[key+'__icontains'] = value    
    datasPrev = Product.objects.filter(**filters).annotate(
                    margin = (F('sell_price')-F('buy_price'))/F('buy_price')*100
                )

    operatorbuy = ''
    operatorbuySign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatorbuy':
                if value == 'e':
                    operatorbuy = ''
                    operatorbuySign = 'e'
                elif value == 'lt':
                    operatorbuy = '__lt'
                    operatorbuySign = 'lt'
                elif value == 'lte':
                    operatorbuy = '__lte'
                    operatorbuySign = 'lte'
                elif value == 'gt':
                    operatorbuy = '__gt'
                    operatorbuySign = 'gt'
                elif value == 'gte':
                    operatorbuy = '__gte'
                    operatorbuySign = 'gte'
    filterOperators = {}
    buy_price = ''
    if 'buy_price' in request.GET:
        if request.GET['buy_price'] != '':
            filterOperators['buy_price'+operatorbuy] = request.GET['buy_price']
            buy_price = request.GET['buy_price']
    datasPrev = datasPrev.filter(**filterOperators)

    operatorsell = ''
    operatorsellSign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatorsell':
                if value == 'e':
                    operatorsell = ''
                    operatorsellSign = 'e'
                elif value == 'lt':
                    operatorsell = '__lt'
                    operatorsellSign = 'lt'
                elif value == 'lte':
                    operatorsell = '__lte'
                    operatorsellSign = 'lte'
                elif value == 'gt':
                    operatorsell = '__gt'
                    operatorsellSign = 'gt'
                elif value == 'gte':
                    operatorsell = '__gte'
                    operatorsellSign = 'gte'
    filterOperators = {}
    sell_price = ''
    if 'sell_price' in request.GET:
        if request.GET['sell_price'] != '':
            filterOperators['sell_price'+operatorsell] = request.GET['sell_price']
            sell_price = request.GET['sell_price']
    datasPrev = datasPrev.filter(**filterOperators)

    operatormargin = ''
    operatormarginSign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatormargin':
                if value == 'e':
                    operatormargin = ''
                    operatormarginSign = 'e'
                elif value == 'lt':
                    operatormargin = '__lt'
                    operatormarginSign = 'lt'
                elif value == 'lte':
                    operatormargin = '__lte'
                    operatormarginSign = 'lte'
                elif value == 'gt':
                    operatormargin = '__gt'
                    operatormarginSign = 'gt'
                elif value == 'gte':
                    operatormargin = '__gte'
                    operatormarginSign = 'gte'
    filterOperators = {}
    margin = ''
    if 'margin' in request.GET:
        if request.GET['margin'] != '':
            filterOperators['margin'+operatormargin] = request.GET['margin']
            margin = request.GET['margin']
    datas = datasPrev.filter(**filterOperators)

    categories = Category.objects.filter()
    suppliers = Supplier.objects.filter()
    print_url = request.scheme+'://'+request.get_host()+request.get_full_path()
    print_url = print_url.replace('product/','product/print/')
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'operatorbuy': operatorbuySign,
        'buy_price': buy_price,
        'operatorsell': operatorsellSign,
        'sell_price': sell_price,
        'operatormargin': operatormarginSign,
        'margin': margin,
        'image_path': image_path,
        'print_url': print_url,
        'datas': datas,
        'categories': categories,
        'suppliers': suppliers,
        'filters': filters
    }
    request.session['menu'] = 'dashboard-product'
    return render(request, 'product/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardProductCreate(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-product'
            return redirect('dashboard-product')
    context = {'form': form}
    request.session['menu'] = 'dashboard-product'
    return render(request, 'product/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardProductEdit(request, id):
    data = Product.objects.get(id=id)
    form = ProductForm(instance=data)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-product'
            return redirect('dashboard-product')
    context = {'form': form}
    request.session['menu'] = 'dashboard-product'
    return render(request, 'product/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardProductDelete(request, id):
    data = Product.objects.get(id=id)
    data.delete()
    messages.error(request, 'Data has been deleted')
    request.session['menu'] = 'dashboard-product'
    return redirect('dashboard-product')

@login_required(login_url='/login/')
def dashboardProductPrint(request):
    category = ''
    supplier = ''
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'category': 
                filters[key] = value
                category = Category.objects.get(id=value)
                category = category.name
            elif key == 'supplier':
                filters[key] = value
                supplier = Supplier.objects.get(id=value)
                supplier = supplier.name
            elif (key == 'operatorbuy') | (key == 'buy_price') | (key == 'operatorsell') | (key == 'sell_price') | (key == 'operatormargin') | (key == 'margin'):
                continue
            else:
                filters[key+'__icontains'] = value    
    datasPrev = Product.objects.filter(**filters).annotate(
                    margin = (F('sell_price')-F('buy_price'))/F('buy_price')*100
                )

    operatorbuy = ''
    operatorbuySign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatorbuy':
                if value == 'e':
                    operatorbuy = ''
                    operatorbuySign = 'e'
                elif value == 'lt':
                    operatorbuy = '__lt'
                    operatorbuySign = 'lt'
                elif value == 'lte':
                    operatorbuy = '__lte'
                    operatorbuySign = 'lte'
                elif value == 'gt':
                    operatorbuy = '__gt'
                    operatorbuySign = 'gt'
                elif value == 'gte':
                    operatorbuy = '__gte'
                    operatorbuySign = 'gte'
    filterOperators = {}
    buy_price = ''
    if 'buy_price' in request.GET:
        if request.GET['buy_price'] != '':
            filterOperators['buy_price'+operatorbuy] = request.GET['buy_price']
            buy_price = request.GET['buy_price']
    datasPrev = datasPrev.filter(**filterOperators)

    operatorsell = ''
    operatorsellSign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatorsell':
                if value == 'e':
                    operatorsell = ''
                    operatorsellSign = 'e'
                elif value == 'lt':
                    operatorsell = '__lt'
                    operatorsellSign = 'lt'
                elif value == 'lte':
                    operatorsell = '__lte'
                    operatorsellSign = 'lte'
                elif value == 'gt':
                    operatorsell = '__gt'
                    operatorsellSign = 'gt'
                elif value == 'gte':
                    operatorsell = '__gte'
                    operatorsellSign = 'gte'
    filterOperators = {}
    sell_price = ''
    if 'sell_price' in request.GET:
        if request.GET['sell_price'] != '':
            filterOperators['sell_price'+operatorsell] = request.GET['sell_price']
            sell_price = request.GET['sell_price']
    datasPrev = datasPrev.filter(**filterOperators)

    operatormargin = ''
    operatormarginSign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatormargin':
                if value == 'e':
                    operatormargin = ''
                    operatormarginSign = 'e'
                elif value == 'lt':
                    operatormargin = '__lt'
                    operatormarginSign = 'lt'
                elif value == 'lte':
                    operatormargin = '__lte'
                    operatormarginSign = 'lte'
                elif value == 'gt':
                    operatormargin = '__gt'
                    operatormarginSign = 'gt'
                elif value == 'gte':
                    operatormargin = '__gte'
                    operatormarginSign = 'gte'
    filterOperators = {}
    margin = ''
    if 'margin' in request.GET:
        if request.GET['margin'] != '':
            filterOperators['margin'+operatormargin] = request.GET['margin']
            margin = request.GET['margin']
    datas = datasPrev.filter(**filterOperators)

    company = Company.objects.first()
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'operatorbuy': operatorbuySign,
        'buy_price': buy_price,
        'operatorsell': operatorsellSign,
        'sell_price': sell_price,
        'operatormargin': operatormarginSign,
        'margin': margin,
        'image_path': image_path,
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'datas': datas,
        'category': category,
        'supplier': supplier,
        'filters': filters
    }
    return to.pdf(request,'product/templates/print.html',context)
