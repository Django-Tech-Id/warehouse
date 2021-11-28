from django.urls import path
from app.modules.customer import views

urlpatterns = [
    path('', views.dashboardCustomer, name='dashboard-customer'),
    path('edit/<id>', views.dashboardCustomerEdit, name='dashboard-customer-edit'),
    path('create/', views.dashboardCustomerCreate, name='dashboard-customer-create'),
    path('delete/<id>', views.dashboardCustomerDelete, name='dashboard-customer-delete'),
    path('print/', views.dashboardCustomerPrint, name='dashboard-customer-print')
]