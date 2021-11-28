from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from app.models import Detail, Transaction
from app.modules.detail.forms import DetailForm
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.db.models import F, Sum
from django.db.models import OuterRef, Subquery, Q
from django.contrib import messages
from decimal import Decimal

MINUS_TRANS = ['Sell','Move Out']
COGS_TRANS = ['Sell', 'Move Out']
MOVEOUT_TRANS = 'Move Out'

# Create your views here.
def dashboardDetailCreate(request):
    if request.method == 'POST':
        print(request.POST)
        form = DetailForm(request.POST)
        if form.is_valid():
            transaction = Transaction.objects.get(id=request.POST['transaction'])
            form = form.save(commit=False)
            if transaction.kind in MINUS_TRANS:
                form.qty = float(request.POST['qty'])*-1
            if transaction.kind in COGS_TRANS:
                qty_check = Transaction.objects.filter(Q(warehousein=request.POST['warehouse']) & (Q(status=None) | Q(status='Accepted'))).aggregate(
                    qty = Sum(F('details__qty'), filter=Q(details__product=request.POST['product']))
                )
                if qty_check['qty'] < float(request.POST['qty']):
                    messages.error(request, 'Quantity unit should be less than available')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    price = 0
                    if settings.COGS_PRICE == 'AVERAGE':
                        total = Transaction.objects.filter(warehousein=request.POST['warehouse']).aggregate(
                            qty = Sum(F('details__qty'), filter=Q(details__product=request.POST['product'])),
                            total = Sum(F('details__qty')* F('details__price'), filter=Q(details__product=request.POST['product'])),
                        )
                        price = float(total['total'])/float(total['qty'])
                    else:
                        qty = Transaction.objects.filter(warehousein=request.POST['warehouse']).aggregate(
                            qty = Sum(F('details__qty'), filter=Q(details__product=request.POST['product']))
                        )
                        details = Detail.objects.filter(transaction=OuterRef('pk')).filter(product=request.POST['product'])
                        price = Transaction.objects.filter(Q(warehousein=request.POST['warehouse'])).filter(Q(kind='Buy')|Q(kind='Move In')).annotate(
                            price=Subquery(details.values('price')[:1])
                        ).order_by('-date')
                        price = price[0].price
            else:
                price = request.POST['price']
            form.price = price
            form.created_by = request.user
            form.save()
            if transaction.kind == MOVEOUT_TRANS:
                transactionMovein = Transaction.objects.get(transaction=transaction)
                detailMovin = DetailForm(request.POST)
                detailMovin = detailMovin.save(commit=False)
                detailMovin.transaction = transactionMovein
                detailMovin.price = form.price
                detailMovin.status = 0
                detailMovin.created_by = request.user
                detailMovin.save()
    messages.error(request, 'Data has been created')
    return redirect(request.META.get('HTTP_REFERER'))

def dashboardDetailEdit(request, id):
    data = Detail.objects.get(id=id)
    data_qty = data.qty
    data_price = data.price
    if request.is_ajax and request.method == 'GET':
        result = serializers.serialize('json', [data])
        response = {
            'status': True,
            'message': 'Success',
            'data': result
        }
        return JsonResponse(response, status=200)
    else:
        if request.method == 'POST':
            form = DetailForm(request.POST, instance=data)
            if form.is_valid():
                transaction = Transaction.objects.get(id=request.POST['transaction'])
                form = form.save(commit=False)
                if transaction.kind in MINUS_TRANS:
                    form.qty = float(request.POST['qty'])*-1
                if transaction.kind in COGS_TRANS:
                    qty_check = Transaction.objects.filter(Q(warehousein=request.POST['warehouse']) & (Q(status=None) | Q(status='Accepted'))).aggregate(
                        qty = Sum(F('details__qty'), filter=Q(details__product=request.POST['product']))
                    )
                    if qty_check['qty']+Decimal(data_qty*-1) < float(request.POST['qty']):
                        messages.error(request, 'Quantity unit should be less than available')
                        return redirect(request.META.get('HTTP_REFERER'))
                form.price = data_price
                form.updated_by = request.user
                form.save()
                #-------------------
                #UPDATE MOVE IN ITEM
                #-------------------
                if transaction.kind == MOVEOUT_TRANS:
                    transactionMovein = Transaction.objects.get(transaction=data.transaction)
                    detailMovein = Detail.objects.get(Q(transaction=transactionMovein) & Q(product=data.product))
                    formDetail = DetailForm(request.POST, instance=detailMovein)
                    formDetail = formDetail.save(commit=False)
                    formDetail.transaction = transactionMovein
                    formDetail.price = form.price
                    formDetail.status = 0
                    formDetail.created_by = request.user
                    formDetail.save()
        messages.error(request, 'Data has been updated')
        return redirect(request.META.get('HTTP_REFERER'))

def dashboardDetailVerify(request, id):
    data = Detail.objects.get(id=id)
    if request.is_ajax and request.method == 'GET':
        if data.status:
            data.status = 0
            messages.success(request, 'Data has been unverified')
        else:
            data.status = 1
            messages.success(request, 'Data has been verified')
        data.updated_by = request.user
        data.save()
    return redirect(request.META.get('HTTP_REFERER'))

def dashboardDetailDelete(request, id):
    data = Detail.objects.get(id=id)
    if data.transaction.kind == MOVEOUT_TRANS:
        transactionMovein = Transaction.objects.get(transaction=data.transaction)
        detailMovein = Detail.objects.get(Q(transaction=transactionMovein) & Q(product=data.product))
        detailMovein.delete()
    data.delete()
    messages.error(request, 'Data has been deleted')
    return redirect(request.META.get('HTTP_REFERER'))
