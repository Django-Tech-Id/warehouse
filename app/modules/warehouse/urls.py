from django.urls import path
from app.modules.warehouse import views

urlpatterns = [
    path('', views.dashboardWarehouse, name='dashboard-warehouse'),
    path('edit/<id>', views.dashboardWarehouseEdit, name='dashboard-warehouse-edit'),
    path('create/', views.dashboardWarehouseCreate, name='dashboard-warehouse-create'),
    path('delete/<id>', views.dashboardWarehouseDelete, name='dashboard-warehouse-delete'),
    path('print/', views.dashboardWarehousePrint, name='dashboard-warehouse-print')
]