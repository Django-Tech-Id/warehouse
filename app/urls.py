# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from app import views
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def Hello(request):
    return HttpResponse('Helllo')
urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('hello/', Hello, name='hello'),
    path('dashboard/', include('app.modules.dashboard.urls')),
    path('dashboard/category/', include('app.modules.category.urls')),
    path('dashboard/warehouse/', include('app.modules.warehouse.urls')),
    path('dashboard/customer/', include('app.modules.customer.urls')),
    path('dashboard/supplier/', include('app.modules.supplier.urls')),
    path('dashboard/product/', include('app.modules.product.urls')),
    path('dashboard/buy/', include('app.modules.buy.urls')),
    path('dashboard/sell/', include('app.modules.sell.urls')),
    path('dashboard/movein/', include('app.modules.movein.urls')),
    path('dashboard/moveout/', include('app.modules.moveout.urls')),
    path('dashboard/detail/', include('app.modules.detail.urls')),
    path('dashboard/company/', include('app.modules.company.urls')),
    path('dashboard/inventory/', include('app.modules.inventory.urls')),
    path('api/', include('app.modules.api.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
