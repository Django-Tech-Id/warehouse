from django.http.response import HttpResponse
from django.urls import path
from app.modules.api import views
from django.views.decorators.csrf import csrf_exempt

def Coba(request):
    return HttpResponse('Hello')

urlpatterns = [
    path('transaction/movein/history/<id>', csrf_exempt(views.apiTransactionMoveinHistory), name='api-transaction-movein-history'),
    path('transaction/movein/register/', csrf_exempt(views.apiTransactionMoveinRegister), name='api-transaction-movein-register'),
    path('transaction/movein/deliver/', csrf_exempt(views.apiTransactionMoveinDeliver), name='api-transaction-movein-deliver'),
    path('warehouse/', csrf_exempt(views.apiWarehouse), name='api-warehouse'),
    # path('', Coba),
    # path('edit/<id>', views.dashboardBuyEdit, name='dashboard-buy-edit'),
    # path('create/', views.dashboardBuyCreate, name='dashboard-buy-create'),
    # path('delete/<id>', views.dashboardBuyDelete, name='dashboard-buy-delete'),
    # path('invoice/<id>', views.dashboardBuyInvoice, name='dashboard-buy-invoice')
]