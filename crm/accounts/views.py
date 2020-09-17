from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')  # restrict this page without login
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'orders_delivered': orders_delivered,
               'orders_pending': orders_pending}

    return render(request, 'accounts/dashboard.html', context)
    #return HttpResponse('This is Home Page')


@login_required(login_url='login')  # restrict this page without login
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')  # restrict this page without login
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    orders_count = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)  # Filter orders based query
    orders = my_filter.qs  # get the filtered orders in variable

    context = {'customer': customer, 'orders': orders, 'orders_count': orders_count, 'my_filter': my_filter}

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')  # restrict this page without login
def create_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)  # take input as entered data and store in a variable
        if form.is_valid():  # check form is valid or not
            form.save()  # save the form in db
            return redirect('/')  # redirect to home page
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')  # restrict this page without login
def update_order(request, id):
    order = Order.objects.get(id=id)  # to pre fill the particular customer
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # take input as entered data and store in a variable
        if form.is_valid():  # check form is valid or not
            form.save()  # save the form in db
            return redirect('/')  # redirect to home page

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')  # restrict this page without login
def remove_order(request, id):
    item = Order.objects.get(id=id)

    if request.method == 'POST':
        item.delete()  # delete the order
        return redirect('/')  # redirect to home page

    context = {'item': item}
    return render(request, 'accounts/remove.html', context)


def login_page(request):
    if request.user.is_authenticated:  # if user already logged in redirect to home page
        return redirect('home')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        elif request.method == 'POST':  # display flash message only when Login Button is Pressed!
            messages.info(request, "Username OR Password is Incorrect!")

        context = {}
        return render(request, 'accounts/login.html', context)


def register(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, user+", your Account is Created!")
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')