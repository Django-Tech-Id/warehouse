from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Transaction, Customer, Supplier, Warehouse, Category, Product
from app.modules.company.forms import CompanyForm
import uuid
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.db.models import OuterRef, Subquery, Q
import calendar
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    start = date(date.today().year, 1, 1)
    end = date(date.today().year, 12, 31)
    first = start
    last = end
    if 'from' in request.GET:
        if request.GET['from'] != '':
            start = request.GET['from']
    if 'to' in request.GET:
        if request.GET['to'] != '':
            end = request.GET['to']
    filters = {
        'date__gte': start,
        'date__lte': end
    }
    transactions = Transaction.objects.filter(**filters)
    transaction = transactions.count()
    buy = transactions.filter(kind='Buy').count()
    sell = transactions.filter(kind='Sell').count()
    moveout = transactions.filter(kind='Move Out').count()
    movein = transactions.filter(kind='Move In').count()
    created = transactions.filter(status='Created').count()
    registered = transactions.filter(status='Registered').count()
    delivered = transactions.filter(status='Delivered').count()
    received = transactions.filter(status='Received').count()
    pending = transactions.filter(status='Pending').count()
    accepted = transactions.filter(status='Accepted').count()
    customer = Customer.objects.all().count()
    supplier = Supplier.objects.all().count()
    warehouse = Warehouse.objects.all().count()
    category = Category.objects.all().count()
    product = Product.objects.all().count()
    product = Product.objects.all().count()
    user = User.objects.all().count()
    buypercentage = (buy/transaction if transaction != 0 else 0)*100
    sellpercentage = (sell/transaction if transaction != 0 else 0)*100
    moveoutpercentage = (moveout/transaction if transaction != 0 else 0)*100

    filters['kind'] = 'Sell'
    sales = Transaction.objects.filter(**filters).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )

    # RINCIAN LABA RUGI BULANAN:
    # 01
    month1 = calendar.monthrange(first.year, 1)[1]
    filter1 = {
        'date__gte': str(first.year)+'-'+str(1)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(1)+'-'+str(month1),
        'kind': 'Sell'
    }
    sales1 = Transaction.objects.filter(**filter1).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly1 = {
        'cost': sales1['cost'],
        'sales': sales1['sales'],
        'income': sales1['income']
    }
    print(sales1)
    # 02
    month2 = calendar.monthrange(first.year, 2)[1]
    filter2 = {
        'date__gte': str(first.year)+'-'+str(2)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(2)+'-'+str(month2),
        'kind': 'Sell'
    }
    sales2 = Transaction.objects.filter(**filter2).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly2 = {
        'cost': sales2['cost'],
        'sales': sales2['sales'],
        'income': sales2['income']
    }
    # 03
    month3 = calendar.monthrange(first.year, 3)[1]
    filter3 = {
        'date__gte': str(first.year)+'-'+str(3)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(3)+'-'+str(month3),
        'kind': 'Sell'
    }
    sales3 = Transaction.objects.filter(**filter3).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly3 = {
        'cost': sales3['cost'],
        'sales': sales3['sales'],
        'income': sales3['income']
    }
    # 04
    month4 = calendar.monthrange(first.year, 4)[1]
    filter4 = {
        'date__gte': str(first.year)+'-'+str(4)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(4)+'-'+str(month4),
        'kind': 'Sell'
    }
    sales4 = Transaction.objects.filter(**filter4).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly4 = {
        'cost': sales4['cost'],
        'sales': sales4['sales'],
        'income': sales4['income']
    }
    # 05
    month5 = calendar.monthrange(first.year, 5)[1]
    filter5 = {
        'date__gte': str(first.year)+'-'+str(5)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(5)+'-'+str(month5),
        'kind': 'Sell'
    }
    sales5 = Transaction.objects.filter(**filter5).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly5 = {
        'cost': sales5['cost'],
        'sales': sales5['sales'],
        'income': sales5['income']
    }
    # 06
    month6 = calendar.monthrange(first.year, 6)[1]
    filter6 = {
        'date__gte': str(first.year)+'-'+str(6)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(6)+'-'+str(month6),
        'kind': 'Sell'
    }
    sales6 = Transaction.objects.filter(**filter6).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly6 = {
        'cost': sales6['cost'],
        'sales': sales6['sales'],
        'income': sales6['income']
    }
    # 07
    month7 = calendar.monthrange(first.year, 7)[1]
    filter7 = {
        'date__gte': str(first.year)+'-'+str(7)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(7)+'-'+str(month7),
        'kind': 'Sell'
    }
    sales7 = Transaction.objects.filter(**filter7).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly7 = {
        'cost': sales7['cost'],
        'sales': sales7['sales'],
        'income': sales7['income']
    }
    # 08
    month8 = calendar.monthrange(first.year, 8)[1]
    filter8 = {
        'date__gte': str(first.year)+'-'+str(8)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(8)+'-'+str(month8),
        'kind': 'Sell'
    }
    sales8 = Transaction.objects.filter(**filter8).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly8 = {
        'cost': sales8['cost'],
        'sales': sales8['sales'],
        'income': sales8['income']
    }
    # 09
    month9 = calendar.monthrange(first.year, 9)[1]
    filter9 = {
        'date__gte': str(first.year)+'-'+str(9)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(9)+'-'+str(month9),
        'kind': 'Sell'
    }
    sales9 = Transaction.objects.filter(**filter9).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly9 = {
        'cost': sales9['cost'],
        'sales': sales9['sales'],
        'income': sales9['income']
    }
    # 10
    month10 = calendar.monthrange(first.year, 10)[1]
    filter10 = {
        'date__gte': str(first.year)+'-'+str(10)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(10)+'-'+str(month10),
        'kind': 'Sell'
    }
    sales10 = Transaction.objects.filter(**filter10).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly10 = {
        'cost': sales10['cost'],
        'sales': sales10['sales'],
        'income': sales10['income']
    }
    # 11
    month11 = calendar.monthrange(first.year, 11)[1]
    filter11 = {
        'date__gte': str(first.year)+'-'+str(11)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(11)+'-'+str(month11),
        'kind': 'Sell'
    }
    sales11 = Transaction.objects.filter(**filter11).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly11 = {
        'cost': sales11['cost'],
        'sales': sales11['sales'],
        'income': sales11['income']
    }
    # 12
    month12 = calendar.monthrange(first.year, 12)[1]
    filter12 = {
        'date__gte': str(first.year)+'-'+str(12)+'-'+str(1),
        'date__lte': str(first.year)+'-'+str(12)+'-'+str(month12),
        'kind': 'Sell'
    }
    sales12 = Transaction.objects.filter(**filter12).aggregate(
        cost = Sum(F('details__qty')* F('details__price'))*-1,
        sales = Sum(F('details__qty')* F('details__price_sell'))*-1,
        income = (Sum(F('details__qty')* F('details__price_sell'))*-1)-(Sum(F('details__qty')* F('details__price'))*-1),
    )
    monthly12 = {
        'cost': sales12['cost'],
        'sales': sales12['sales'],
        'income': sales12['income']
    }

    incomes = {
        1:monthly1,
        2:monthly2,
        3:monthly3,
        4:monthly4,
        5:monthly5,
        6:monthly6,
        7:monthly7,
        8:monthly8,
        9:monthly9,
        10:monthly10,
        11:monthly11,
        12:monthly12,
    }
    # END RINCIAN LABA RUGI BULANAN:
    context = {
        'buy': buy,
        'sell': sell,
        'moveout': moveout,
        'movein': movein,
        'created': created,
        'registered': registered,
        'delivered': delivered,
        'received': received,
        'pending': pending,
        'accepted': accepted,
        'customer': customer,
        'supplier': supplier,
        'warehouse': warehouse,
        'category': category,
        'product': product,
        'user': user,
        'buypercentage': buypercentage,
        'sellpercentage': sellpercentage,
        'moveoutpercentage': moveoutpercentage,
        'income': sales['income'],
        'expense': sales['cost'],
        'transaction': transaction,
        'sales': sales['sales'],
        'from': start,
        'to': end,
        'incomes': incomes
    }
    request.session['menu'] = 'dashboard'
    return render(request, 'dashboard/templates/index.html', context)
