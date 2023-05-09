from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from cart.models import *
from accounts.models import *
from admin_products.models import *
import math
import datetime
from django.utils import timezone
from operator import countOf

# Create your views here.

User = get_user_model()


def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        cart = OldCart.objects.all()
        orders = Order.objects.all()
        order_count = 0
        revenue = 0

        for i in cart:
            order_count = order_count+1
            revenue = revenue + i.total
        product = Products.objects.all()
        product_count = Products.objects.all().count()

        # user count
        user_count = User.objects.exclude(username='admin').count()

        # weekely

        weekly = Order.objects.all()
        datepicker = timezone.now()
        date_list = []
        sales_list = []
        sales = 0
        for i in range(7):

            date_list.append(datepicker.date())
            datepicker = datepicker - datetime.timedelta(days=1)
        for i in date_list:
            for j in weekly:

                if i == j.ordered_date.date():

                    sales = sales + j.amount
                    print(i, j.amount)
            sales_list.append(sales)
            sales = 0
        print(sales_list)
        print(date_list)

        return render(request, 'dashboard.html',
                      {'revenue': revenue, 'order_count': order_count, 'product': product, 'cart': cart,
                       'product_count': product_count, 'user_count': user_count, 'date_list': date_list, 'sales_list': sales_list, 'orders': orders})
    else:
        return redirect('admin_login')


@never_cache
def admin_login(request):

    if request.user.is_authenticated:
        return redirect(dashboard)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect(dashboard)

        else:
            messages.info(request, 'Enter Proper Username Or Password')
            return redirect(admin_login)

    return render(request, 'admin_login.html')


@never_cache
def admin_logout(request):

    if request.user.is_superuser:
        logout(request)
    return redirect(admin_login)


def user_list(request):

    if request.user.is_authenticated and request.user.is_superuser:
        user_count = User.objects.exclude(username='afrinjasim').count()

        if 'search' in request.GET:
            search = request.GET['search']
            multiple_search = Q(Q(full_name__icontains=search) | Q(username__icontains=search) | Q(
                phone_number__icontains=search) | Q(email__icontains=search))
            user_list = User.objects.filter(multiple_search)

        else:
            user_list = User.objects.all()

        context = {
            "user_list": user_list,
            'user_count': user_count
        }
        return render(request, 'user-list.html', context)
    return redirect(admin_login)


def block_user(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect(user_list)

    return redirect(admin_login)


def unblock_user(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect(user_list)
    return redirect(admin_login)


def wallet_details(request):
    if request.user.is_superuser:
        wal_details = Wallet.objects.all()
        return render(request, 'wallet_details.html', {"wal_details": wal_details})
    return redirect(admin_login)
