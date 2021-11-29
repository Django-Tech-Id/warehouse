from django.http.response import HttpResponse
from app.models import Status, Transaction, Warehouse
from app.modules.status.forms import StatusForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import OuterRef, Subquery, Q
from uuid import UUID
from app.functions import validate

def apiTransactionMoveinRegister(request):
    if request.method == 'GET':
        response = {
            'code': 400,
            'status': False,
            'message': 'Get method is not allowed',
        }
        return JsonResponse(response, status=400)
    else:
        if (not 'id' in request.POST) | (not 'rfid' in request.POST):
            response = {
                'code': 400,
                'status': False,
                'message': 'Parameter id and rfid should be included',
            }
            return JsonResponse(response, status=400)
        elif (request.POST['id'] is None) | (request.POST['rfid'] is None):
            response = {
                'code': 400,
                'status': False,
                'message': 'Parameter id and rfid should not be blank',
            }
            return JsonResponse(response, status=400)
        else:
            if not validate.uuid(request.POST['id']):
                response = {
                    'code': 400,
                    'status': False,
                    'message': 'UUID is not valid',
                }
                return JsonResponse(response, status=400)
            else:
                if not Transaction.objects.filter(id=request.POST['id']).exists():
                    response = {
                        'code': 404,
                        'status': False,
                        'message': 'Transaction is not found',
                    }
                    return JsonResponse(response, status=404)
                else:
                    if not Transaction.objects.filter(id=request.POST['id']).exists():
                        response = {
                            'code': 404,
                            'status': False,
                            'message': 'Data is not found',
                        }
                        return JsonResponse(response, status=404)
                    else:
                        data = Transaction.objects.get(id=request.POST['id'])
                        rfid = request.POST['rfid']
                        dataMovein = data.transactions.get()
                        if dataMovein.statuses.filter(status='Registered').exists():
                            response = {
                                'code': 403,
                                'status': False,
                                'message': 'RFID already registered',
                            }
                            return JsonResponse(response, status=403)
                        else:

                            #====================
                            #PEMBUATAN RFID
                            #====================

                            dataMovein.status = 'Registered'
                            dataMovein.rfid = rfid
                            dataMovein.description = 'RFID already registered at '+dataMovein.warehouseout.name
                            dataMovein.save()

                            statusForm = StatusForm()
                            statusForm = statusForm.save(commit=False)
                            statusForm.transaction = dataMovein
                            statusForm.status = 'Registered'
                            statusForm.warehouse = dataMovein.warehouseout
                            statusForm.description = 'RFID already registered at '+dataMovein.warehouseout.name
                            statusForm.save()

                            details = dataMovein.details.all()
                            total = 0
                            items = []
                            for detail in details:
                                item = {
                                    'product': str(detail.product),
                                    'qty': float(detail.qty),
                                    'price': float(detail.price),
                                    'status': detail.status
                                }
                                items.append(item)
                                total += (detail.qty*detail.price)

                            dataResponse = {
                                'id': str(data.id),
                                'code': dataMovein.code,
                                'from': str(dataMovein.warehouseout),
                                'to': str(dataMovein.warehousein),
                                'status': 'Registered',
                                'total': total,
                                'description': statusForm.description,
                                'items': items
                            }

                            response = {
                                'code': 200,
                                'status': True,
                                'message': 'Data is created successfully',
                                'data': dataResponse
                            }
                            return JsonResponse(response, status=200)


def apiTransactionMoveinDeliver(request):
    if request.method == 'GET':
        response = {
            'code': 400,
            'status': False,
            'message': 'Get method is not allowed',
        }
        return JsonResponse(response, status=400)
    else:
        if (not 'rfid' in request.POST) | (not 'warehouseid' in request.POST):
            response = {
                'code': 400,
                'status': False,
                'message': 'Parameter rfid and warehouseid should be included',
            }
            return JsonResponse(response, status=400)
        elif (request.POST['rfid'] is None) | (request.POST['warehouseid'] is None):
            response = {
                'code': 400,
                'status': False,
                'message': 'Parameter rfid and warehouseid should not be blank',
            }
            return JsonResponse(response, status=400)
        else:
            if (not validate.uuid(request.POST['warehouseid'])):
                response = {
                    'code': 400,
                    'status': False,
                    'message': 'UUID is not valid',
                }
                return JsonResponse(response, status=400)
            else:
                if not Transaction.objects.filter(rfid=request.POST['rfid']).exists():
                    response = {
                        'code': 404,
                        'status': False,
                        'message': 'Transaction is not found',
                    }
                    return JsonResponse(response, status=404)
                elif not Warehouse.objects.filter(id=request.POST['warehouseid']).exists():
                    response = {
                        'code': 404,
                        'status': False,
                        'message': 'Warehouse is not found',
                    }
                    return JsonResponse(response, status=404)
                else:
                    data = Transaction.objects.get(rfid=request.POST['rfid'])
                    warehouse = Warehouse.objects.get(id=request.POST['warehouseid'])
                    if not data.statuses.filter(Q(status='Registered')).exists():
                        response = {
                            'code': 404,
                            'status': False,
                            'message': 'RFID has not been registered, please register first',
                        }
                        return JsonResponse(response, status=403)
                    else:
                        if data.statuses.filter(Q(status='Delivered') & Q(warehouse=warehouse)).exists():
                            response = {
                                'code': 403,
                                'status': False,
                                'message': 'Item has been delivered to '+warehouse.name,
                            }
                            return JsonResponse(response, status=403)
                        elif data.statuses.filter(Q(status='Received') & Q(warehouse=warehouse)).exists():
                            response = {
                                'code': 403,
                                'status': False,
                                'message': 'Item has been received to '+warehouse.name,
                            }
                            return JsonResponse(response, status=403)
                        else:
                            #====================
                            #PENGIRIMAN BARANG RFID
                            #====================
                            if data.warehousein.id == warehouse.id:                            
                                data.status = 'Received'
                                data.description = 'Inventory has been received at '+warehouse.name,
                            else:
                                data.status = 'Delivered'
                                data.description = 'Inventory has been delivered to '+warehouse.name,
                            data.save()

                            statusForm = StatusForm()
                            statusForm = statusForm.save(commit=False)
                            statusForm.transaction = data
                            statusForm.warehouse = warehouse
                            if data.warehousein.id == warehouse.id:                            
                                statusForm.status = 'Received'
                                statusForm.description = 'Inventory has been received at '+warehouse.name,
                            else:
                                statusForm.status = 'Delivered'
                                statusForm.description = 'Inventory has been delivered to '+warehouse.name,
                            statusForm.save()

                            details = data.details.all()
                            total = 0
                            items = []
                            for detail in details:
                                item = {
                                    'product': str(detail.product),
                                    'qty': float(detail.qty),
                                    'price': float(detail.price),
                                    'status': detail.status
                                }
                                items.append(item)
                                total += (detail.qty*detail.price)

                            dataResponse = {
                                'id': str(data.id),
                                'code': data.code,
                                'from': str(data.warehouseout),
                                'to': str(data.warehousein),
                                'status': 'Delivered',
                                'total': total,
                                'description': statusForm.description,
                                'items': items
                            }

                            response = {
                                'code': 200,
                                'status': True,
                                'message': 'Data is created successfully',
                                'data': dataResponse
                            }
                            return JsonResponse(response, status=200)

def apiTransactionMoveinHistory(request,id):
    if request.method == 'POST':
        response = {
            'code': 400,
            'status': False,
            'message': 'Post method is not allowed',
        }
        return JsonResponse(response, status=400)
    else:
        if (not validate.uuid(id)):
            response = {
                'code': 400,
                'status': False,
                'message': 'UUID is not valid',
            }
            return JsonResponse(response, status=400)
        else:
            if not Transaction.objects.filter(id=id).exists():
                response = {
                    'code': 404,
                    'status': False,
                    'message': 'Transaction is not found',
                }
                return JsonResponse(response, status=404)
            else:
                transaction = Transaction.objects.get(id=id)
                statuses = transaction.statuses.all().order_by('-created_at')
                items = []
                for status in statuses:
                    item = {
                        'date': status.created_at,
                        'status': status.status,
                        'warehouse': status.warehouse.name,
                        'description': status.description
                    }
                    items.append(item)

                response = {
                    'code': 200,
                    'status': True,
                    'message': 'List of statuses',
                    'data': items
                }
                return JsonResponse(response, status=200)

def apiWarehouse(request):
    if request.method == 'POST':
        response = {
            'code': 400,
            'status': False,
            'message': 'Post method is not allowed',
        }
        return JsonResponse(response, status=400)
    else:
        warehouses = Warehouse.objects.filter(Q(status=1))
        items = []
        for detail in warehouses:
            item = {
                'id': detail.id,
                'name': detail.name,
                'address': detail.address,
                'description': detail.description
            }
            items.append(item)

        response = {
            'code': 200,
            'status': True,
            'message': 'List of warehouses',
            'data': items
        }
        return JsonResponse(response, status=200)