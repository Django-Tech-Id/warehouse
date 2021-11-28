from django.urls import path
from app.modules.movein import views

urlpatterns = [
    path('', views.dashboardMovein, name='dashboard-movein'),
    path('edit/<id>', views.dashboardMoveinEdit, name='dashboard-movein-edit'),
    path('invoice/<id>', views.dashboardMoveinInvoice, name='dashboard-movein-invoice'),
    path('print/', views.dashboardMoveinPrint, name='dashboard-movein-print'),
]