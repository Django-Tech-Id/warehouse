from django.urls import path
from app.modules.product import views

urlpatterns = [
    path('', views.dashboardProduct, name='dashboard-product'),
    path('edit/<id>', views.dashboardProductEdit, name='dashboard-product-edit'),
    path('create/', views.dashboardProductCreate, name='dashboard-product-create'),
    path('delete/<id>', views.dashboardProductDelete, name='dashboard-product-delete'),
    path('print/', views.dashboardProductPrint, name='dashboard-product-print')
]