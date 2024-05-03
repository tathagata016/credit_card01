from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.

def index(request):
    return render(request, "index_home.html")

def index_about(request):
    data = About.objects.all()
    d = {'data': data}
    return render(request, "index_about.html", d)

def index_contact(request):
    data = Contact.objects.all()
    d = {'data': data}
    return render(request, "index_contact.html", d)

def dashboard(request):
    admin = Subbanker.objects.all()
    new = Application.objects.filter(status="Not Updated Yet")
    appr = Application.objects.filter(status="Approved")
    rej = Application.objects.filter(status="Rejected")
    return render(request, "admin_dashboard.html", locals())

def authentication_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            if user:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            else:
                messages.success(request, "Invalid User")
                return redirect('authentication_login')
        except:
            messages.success(request, "Invalid User")
            return redirect('authentication_login')
    return render(request, "authentication-login.html")

@login_required(login_url='/authentication_login/')
def change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')

    return render(request, 'change_password.html')

@login_required(login_url='/authentication_login/')
def logout_user(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('authentication_login')

@login_required(login_url='/authentication_login/')
def add_subadmin(request, pid=None):
    user = None
    subbanker = None
    if pid:
        user = User.objects.get(id=pid)
        subbanker = Subbanker.objects.get(user=user)
    if request.method == "POST":
        form = SubbankerForm(request.POST, request.FILES, instance=subbanker)
        if form.is_valid():
            new_subbanker = form.save()
            if pid:
                new_user = User.objects.filter(id=pid).update(email=request.POST['email'], first_name=request.POST['firstname'])
                Subbanker.objects.filter(user=request.user).update(mobile=request.POST['mobile'])
            else:
                new_user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['firstname'], email=request.POST['email'], password=request.POST['password'],)
                new_subbanker.user = new_user
                new_subbanker.save()
        messages.success(request, "Registration Successful")
        return redirect('view_subadmin')
    return render(request, 'add_subadmin.html', locals())

@login_required(login_url='/authentication_login/')
def view_subadmin(request):
    data = Subbanker.objects.all()
    d = {'data': data}
    return render(request, "view_subadmin.html", d)

@login_required(login_url='/authentication_login/')
def delete_subadmin(request, pid):
    data = Subbanker.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_subadmin')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def add_application(request, pid=None):
    application = None
    if pid:
        application = Application.objects.get(id=pid)
    if request.method == "POST":
        apply = ApplicationForm(request.POST, request.FILES, instance=application)
        if apply.is_valid():
            new_application = apply.save()
            if not pid:
                new_application.regnumber = random_with_N_digits(10)
            new_application.save()
        messages.success(request, "Credit card application request has been sent successfully.Application Number is " + str(new_application.regnumber))
        return redirect('/')
    return render(request, '', locals())

@login_required(login_url='/authentication_login/')
def applicationlist(request):
    action = request.GET.get('action')
    if action == "New":
        data = Application.objects.filter(status='Not Updated Yet')
    elif action == "Approved":
        data = Application.objects.filter(status='Approved')
    elif action == "Rejected":
        data = Application.objects.filter(status='Rejected')
    elif action == "All":
        data = Application.objects.filter()
    d = {'data': data}
    return render(request, "applicationlist.html", d)

@login_required(login_url='/authentication_login/')
def delete_application(request, pid):
    data = Application.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_application')

def detail(request,pid):
    data = Application.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        limit = request.POST['limit']
        status = request.POST['status']
        data.status = status
        data.save()
        abc = Application.objects.update(limit=limit)
        Trackinghistory.objects.create(application=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('detail', pid)
    traking = Trackinghistory.objects.filter(application=data)
    return render(request, "detail.html", locals())

def index_search(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Application.objects.filter(Q(fullname__icontains=fromdate)|Q (mobile__icontains=fromdate)|Q (email__icontains=fromdate)|Q (regnumber__icontains=fromdate))
    return render(request, "index_search.html", locals())

@login_required(login_url='/authentication_login/')
def report_date(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Application.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "report_date.html", locals())

@login_required(login_url='/authentication_login/')
def search_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Application.objects.filter(Q(fullname__icontains=fromdate)|Q (regnumber__icontains=fromdate))
    return render(request, "search_report.html", locals())

@login_required(login_url='/authentication_login/')
def about(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        About.objects.filter(id=1).update(pagetitle=pagetitle, description=description)
        messages.success(request, "Update About Successful")
        return redirect('about')
    data = About.objects.get(id=1)
    return render(request, "about.html", locals())

@login_required(login_url='/admin_login/')
def contact(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        email = request.POST['email']
        mobile = request.POST['mobile']

        Contact.objects.filter(id=1).update(pagetitle=pagetitle, description=description, email=email, mobile=mobile)
        messages.success(request, "Update Contact Successful")
        return redirect('contact')
    data = Contact.objects.get(id=1)
    return render(request, "contact.html", locals())

@login_required(login_url='/authentication_login/')
def profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        email = request.POST['email']
        uname = request.POST['username']
        mobile = request.POST['mobile']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, email=email, username=uname)
        Subbanker.objects.filter(user=request.user).update(mobile=mobile)
        messages.success(request, "Updation Successful")
        return redirect('profile')
    data = Subbanker.objects.get(user=request.user)
    return render(request, "profile.html", locals())

