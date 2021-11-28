from django.urls import path
from app.modules.detail import views

urlpatterns = [
    path('edit/<id>', views.dashboardDetailEdit, name='dashboard-detail-edit'),
    path('verify/<id>', views.dashboardDetailVerify, name='dashboard-detail-verify'),
    path('create/', views.dashboardDetailCreate, name='dashboard-detail-create'),
    path('delete/<id>', views.dashboardDetailDelete, name='dashboard-detail-delete')
]