from django.urls import path
from app.modules.company import views

urlpatterns = [
    path('edit/<id>', views.dashboardCompanyEdit, name='dashboard-company-edit'),
    path('create/', views.dashboardCompanyCreate, name='dashboard-company-create'),
]