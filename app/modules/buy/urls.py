from django.urls import path
from app.modules.buy import views

urlpatterns = [
    path('', views.dashboardBuy, name='dashboard-buy'),
    path('edit/<id>', views.dashboardBuyEdit, name='dashboard-buy-edit'),
    path('create/', views.dashboardBuyCreate, name='dashboard-buy-create'),
    path('delete/<id>', views.dashboardBuyDelete, name='dashboard-buy-delete'),
    path('invoice/<id>', views.dashboardBuyInvoice, name='dashboard-buy-invoice'),
    path('print/', views.dashboardBuyPrint, name='dashboard-buy-print')
]