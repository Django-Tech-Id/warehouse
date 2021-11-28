from django.urls import path
from app.modules.moveout import views

urlpatterns = [
    path('', views.dashboardMoveout, name='dashboard-moveout'),
    path('edit/<id>', views.dashboardMoveoutEdit, name='dashboard-moveout-edit'),
    path('create/', views.dashboardMoveoutCreate, name='dashboard-moveout-create'),
    path('delete/<id>', views.dashboardMoveoutDelete, name='dashboard-moveout-delete'),
    path('invoice/<id>', views.dashboardMoveoutInvoice, name='dashboard-moveout-invoice'),
    path('print/', views.dashboardMoveoutPrint, name='dashboard-moveout-print'),
]