# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date
from app.functions import to
# Create your models here.

def company_location(instance, filename):
    today = date.today()
    *filebase, extension = filename.split('.')
    title = str(instance.name)
    title = title.split(' ')
    title = '-'.join(title)
    title = title.split('.')
    title = ('-'.join(title)).lower()
    id = uuid.uuid4()
    new_file_name = title+'-'+str(id)+'-'+'.'+extension
    return 'company/'+today.strftime('%Y')+'/'+today.strftime('%m')+'/'+today.strftime('%d')+'/'+new_file_name

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=company_location, null=True, blank=True)
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
        
class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def category_location(instance, filename):
    today = date.today()
    *filebase, extension = filename.split('.')
    title = str(instance.name)
    title = title.split(' ')
    title = '-'.join(title)
    title = title.split('.')
    title = ('-'.join(title)).lower()
    id = uuid.uuid4()
    new_file_name = title+'-'+str(id)+'-'+'.'+extension
    return 'category/'+today.strftime('%Y')+'/'+today.strftime('%m')+'/'+today.strftime('%d')+'/'+new_file_name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True, blank=True)
    image = models.ImageField(upload_to=category_location, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def product_location(instance, filename):
    today = date.today()
    *filebase, extension = filename.split('.')
    title = str(instance.name)
    title = title.split(' ')
    title = '-'.join(title)
    title = title.split('.')
    title = ('-'.join(title)).lower()
    id = uuid.uuid4()
    new_file_name = title+'-'+str(id)+'-'+'.'+extension
    return 'product/'+today.strftime('%Y')+'/'+today.strftime('%m')+'/'+today.strftime('%d')+'/'+new_file_name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, null=False)
    supplier = models.ForeignKey(Supplier, related_name='suppliers', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spesification = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True, blank=True)
    image = models.ImageField(upload_to=product_location, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

KIND_TRANSACTION = (
    ('Buy', 'Buy'),
    ('Sell', 'Sell'),
    ('Move In', 'Move In'),
    ('Move Out', 'Move Out')
)

STATUS_TRANSACTION = (
    ('Created', 'Created'),
    ('Registered', 'Registered'),
    ('Delivered', 'Delivered'),
    ('Received', 'Received'),
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted')
)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey('self', related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    kind = models.CharField(max_length=10, choices=KIND_TRANSACTION)
    date = models.DateField(editable=True, null=True)
    pending_date = models.DateField(editable=True, null=True, blank=True)
    accepted_date = models.DateField(editable=True, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, related_name='suppliertransactions', on_delete=models.PROTECT, null=True, blank=True)
    customer = models.ForeignKey(Customer, related_name='customertransactions', on_delete=models.PROTECT, null=True, blank=True)
    warehousein = models.ForeignKey(Warehouse, related_name='warehouseintransactions', on_delete=models.PROTECT, null=True, blank=True)
    warehouseout = models.ForeignKey(Warehouse, related_name='warehouseouttransactions', on_delete=models.PROTECT, null=True, blank=True)
    code = models.CharField(max_length=50)
    rfid = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, choices=STATUS_TRANSACTION)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Detail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='details', on_delete=models.PROTECT)
    qty = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def qty_min(self):
        return self.qty*-1

    @property
    def price_rp(self):
        return to.rupiah('{:.2f}'.format(self.price))

    @property
    def price_sell_rp(self):
        return to.rupiah('{:.2f}'.format(self.price_sell))

    @property
    def total_rp(self):
        return to.rupiah('{:.2f}'.format(self.qty*self.price))

    @property
    def total_sell_rp(self):
        return to.rupiah('{:.2f}'.format(self.qty*self.price_sell*-1))
    # def __str__(self):
    #     return self.product.name

    @property
    def total_min_rp(self):
        return to.rupiah('{:.2f}'.format(self.qty*self.price*-1))
    # def __str__(self):
    #     return self.product.name

class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, related_name='statuses', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, null=True, blank=True, choices=STATUS_TRANSACTION)
    warehouse = models.ForeignKey(Warehouse, related_name='warehousestatuses', on_delete=models.PROTECT, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)