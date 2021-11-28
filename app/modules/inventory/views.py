from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Category, Product, Supplier, Company
import uuid
from django.contrib import messages
from app.functions import to, validate
from django.db.models import F, Sum
from django.db.models import OuterRef, Subquery, Q
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardInventory(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if (key == 'category') | (key == 'supplier'):
                filters[key] = value   
            elif (key == 'operatorqty') | (key == 'qty') | (key == 'operatorbuy') | (key == 'buy_price') | (key == 'operatorsell') | (key == 'sell_price') | (key == 'operatormargin') | (key == 'margin'):
                continue
            else:
                filters[key+'__icontains'] = value    
    datasPrev = Product.objects.filter(**filters).annotate(
        qty = Sum(F('details__qty')),
        price = Sum(F('details__qty')* F('details__price'))/Sum(F('details__qty')),
        total = Sum(F('details__qty')* F('details__price')),
        margin = ((F('sell_price')-(Sum(F('details__qty')* F('details__price'))/Sum(F('details__qty'))))/(Sum(F('details__qty')* F('details__price'))/Sum(F('details__qty'))))*100
    )

    operatorqty = ''
    operatorqtySign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatorqty':
                if value == 'e':
                    operatorqty = ''
                    operatorqtySign = 'e'
                elif value == 'lt':
                    operatorqty = '__lt'
                    operatorqtySign = 'lt'
                elif value == 'lte':
                    operatorqty = '__lte'
                    operatorqtySign = 'lte'
                elif value == 'gt':
                    operatorqty = '__gt'
                    operatorqtySign = 'gt'
                elif value == 'gte':
                    operatorqty = '__gte'
                    operatorqtySign = 'gte'
    filterOperators = {}
    qty = ''
    if 'qty' in request.GET:
        if request.GET['qty'] != '':
            filterOperators['qty'+operatorqty] = request.GET['qty']
            qty = request.GET['qty']
    datasPrev = datasPrev.filter(**filterOperators)

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
            filterOperators['price'+operatorbuy] = request.GET['buy_price']
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
    print_url = print_url.replace('inventory/','inventory/print/')
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'operatorqty': operatorqtySign,
        'qty': qty,
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
    request.session['menu'] = 'dashboard-inventory'
    return render(request, 'inventory/templates/index.html', context)

@login_required(login_url='/login/')
def dashboardInventoryPrint(request):
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
            elif (key == 'operatorqty') | (key == 'qty') | (key == 'operatorbuy') | (key == 'buy_price') | (key == 'operatorsell') | (key == 'sell_price') | (key == 'operatormargin') | (key == 'margin'):
                continue
            else:
                filters[key+'__icontains'] = value    
    datasPrev = Product.objects.filter(**filters).annotate(
        qty = Sum(F('details__qty')),
        price = Sum(F('details__qty')* F('details__price'))/Sum(F('details__qty')),
        total = Sum(F('details__qty')* F('details__price')),
        margin = ((F('sell_price')-(Sum(F('details__qty')* F('details__price'))/Sum(F('details__qty'))))/(Sum(F('details__qty')* F('details__price'))/Sum(F('details__qty'))))*100
    )

    operatorqty = ''
    operatorqtySign = ''
    for key, value in request.GET.items():
        if value != '':
            if key == 'operatorqty':
                if value == 'e':
                    operatorqty = ''
                    operatorqtySign = 'e'
                elif value == 'lt':
                    operatorqty = '__lt'
                    operatorqtySign = 'lt'
                elif value == 'lte':
                    operatorqty = '__lte'
                    operatorqtySign = 'lte'
                elif value == 'gt':
                    operatorqty = '__gt'
                    operatorqtySign = 'gt'
                elif value == 'gte':
                    operatorqty = '__gte'
                    operatorqtySign = 'gte'
    filterOperators = {}
    qty = ''
    if 'qty' in request.GET:
        if request.GET['qty'] != '':
            filterOperators['qty'+operatorqty] = request.GET['qty']
            qty = request.GET['qty']
    datasPrev = datasPrev.filter(**filterOperators)

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
            filterOperators['price'+operatorbuy] = request.GET['buy_price']
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
    print_url = print_url.replace('inventory/','inventory/print/')

    company = Company.objects.first()
    image_path = request.scheme+'://'+request.get_host()
    context = {
        'operatorqty': operatorqtySign,
        'qty': qty,
        'operatorbuy': operatorbuySign,
        'buy_price': buy_price,
        'operatorsell': operatorsellSign,
        'sell_price': sell_price,
        'operatormargin': operatormarginSign,
        'margin': margin,
        'image_path': image_path,
        'print_url': print_url,
        'host': str(request.scheme)+'://'+str(request.get_host()),
        'company': company,
        'datas': datas,
        'category': category,
        'supplier': supplier,
        'filters': filters
    }
    return to.pdf(request,'inventory/templates/print.html',context)