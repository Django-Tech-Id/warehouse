from django.urls import path
from app.modules.supplier import views

urlpatterns = [
    path('', views.dashboardSupplier, name='dashboard-supplier'),
    path('edit/<id>', views.dashboardSupplierEdit, name='dashboard-supplier-edit'),
    path('create/', views.dashboardSupplierCreate, name='dashboard-supplier-create'),
    path('delete/<id>', views.dashboardSupplierDelete, name='dashboard-supplier-delete'),
    path('print/', views.dashboardSupplierPrint, name='dashboard-supplier-print')
]