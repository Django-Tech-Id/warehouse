from django.urls import path
from app.modules.category import views

urlpatterns = [
    path('', views.dashboardCategory, name='dashboard-category'),
    path('edit/<id>', views.dashboardCategoryEdit, name='dashboard-category-edit'),
    path('create/', views.dashboardCategoryCreate, name='dashboard-category-create'),
    path('delete/<id>', views.dashboardCategoryDelete, name='dashboard-category-delete'),
    path('print/', views.dashboardCategoryPrint, name='dashboard-category-print')
]