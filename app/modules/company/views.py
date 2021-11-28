from datetime import datetime
from django.shortcuts import render, redirect

from app.models import Company
from app.modules.company.forms import CompanyForm
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def dashboardCompanyCreate(request):
    company = Company.objects.all()
    if company.exists():
        return redirect('dashboard-company-edit', company[0].id)
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.error(request, 'Data has been created')
            request.session['menu'] = 'dashboard-company'
            return redirect('dashboard-company-edit',form.id)
    context = {'form': form}
    request.session['menu'] = 'dashboard-company'
    return render(request, 'company/templates/form.html', context)

@login_required(login_url='/login/')
def dashboardCompanyEdit(request, id):
    data = Company.objects.get(id=id)
    form = CompanyForm(instance=data)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form = form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.error(request, 'Data has been updated')
            request.session['menu'] = 'dashboard-company'
            return redirect('dashboard-company-edit',id)
    context = {'form': form}
    request.session['menu'] = 'dashboard-company'
    return render(request, 'company/templates/form.html', context)