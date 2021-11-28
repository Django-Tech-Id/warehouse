from django.urls import path
from app.modules.dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]