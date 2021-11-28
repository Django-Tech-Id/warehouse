from django.urls import path
from app.modules.inventory import views

urlpatterns = [
    path('', views.dashboardInventory, name='dashboard-inventory'),
    path('print/', views.dashboardInventoryPrint, name='dashboard-inventory-print'),
]