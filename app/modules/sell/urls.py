from django.urls import path
from app.modules.sell import views

urlpatterns = [
    path('', views.dashboardSell, name='dashboard-sell'),
    path('edit/<id>', views.dashboardSellEdit, name='dashboard-sell-edit'),
    path('create/', views.dashboardSellCreate, name='dashboard-sell-create'),
    path('delete/<id>', views.dashboardSellDelete, name='dashboard-sell-delete'),
    path('invoice/<id>', views.dashboardSellInvoice, name='dashboard-sell-invoice'),
    path('print/', views.dashboardSellPrint, name='dashboard-sell-print')
]