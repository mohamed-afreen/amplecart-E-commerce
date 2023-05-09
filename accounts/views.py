from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import never_cache
from .models import *
from django.contrib.auth import get_user_model
from accounts.CustomBackend import *
from accounts.mixins import MessageHandler
from django.db.models import Q
import random
from admin_products.models import *
from cart.models import *
from django.http import JsonResponse, HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import FileResponse
from decimal import *


# Create your views here.

@never_cache
def user_login(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active == True:
            if 'guest_key' in request.session:
                p = request.session['guest_key']
                guest_cart = guestCart.objects.filter(user_ref=p)

                auth.login(request, user)
                for i in guest_cart:
                    try:
                        cart = Cart.objects.get(
                            user=request.user, product=i.product)
                        print(cart)
                    except:
                        cart = None
                    if cart:
                        print("one")
                        Cart.objects.filter(
                            user=request.user, product=i.product)
                    else:
                        print("two")
                        k = Cart(user=request.user, product=i.product)
                        k.save()
                guest_cart.delete()

            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Wrong UserName or Password')
            return redirect('user_login')

    return render(request, 'login.html')


@never_cache
def sign_up(request):
    if request.method == 'POST':

        new_full_name = request.POST['full_name']
        new_username = request.POST['username']
        new_email = request.POST['email']
        new_phone_number = request.POST['phone_number']
        if '+91' in new_phone_number:
            print("+91 in phone number")
        else:
            new_phone_number = '+91'+new_phone_number
            print("new number = ", new_phone_number)
        new_password1 = request.POST['password1']
        new_password2 = request.POST['password2']

        if new_password1 == new_password2:
            if User.objects.filter(email=new_email).exists():
                messages.error(request, 'Email Is Already taken !')
                return redirect('sign_up')
            elif User.objects.filter(phone_number=new_phone_number).exists():
                messages.error(request, ' Number is already used !')
                return redirect('sign_up')
            elif User.objects.filter(username=new_username).exists():
                messages.error(request, 'Username taken')
                return redirect('sign_up')

            else:

                otp = 123456
                message_handler = MessageHandler(
                    new_phone_number, otp).sent_otp_on_phone()
                return render(request, 'number_otp_verify.html', {'new_full_name': new_full_name, 'new_username': new_username, 'new_email': new_email,
                                                                  'new_phone_number': new_phone_number, 'new_password2': new_password2})
        else:
            messages.error(request, 'Password not matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def number_otp_verify(request):
    if request.method == 'POST':
        new_full_name = request.POST['full_name']
        new_username = request.POST['username']
        new_email = request.POST['email']
        new_phone_number = request.POST['phone_number']
        if '+91' in new_phone_number:
            print("+91 in phone number")
        else:
            new_phone_number = '+91'+new_phone_number
            print("new number = ", new_phone_number)
        new_password2 = request.POST['password2']
        otp1 = int(request.POST['otp'])
        print("new=", new_phone_number)
        validate = MessageHandler(new_phone_number, otp1).validate()
        print("validate=", validate)
        if validate == "approved":

            user = User.objects.create_user(full_name=new_full_name, username=new_username,
                                            password=new_password2, email=new_email, phone_number=new_phone_number)
            user.save()

            get_user = User.objects.get(username=new_username)
            wallet = Wallet.objects.create(user=get_user)
            wallet.save()

            if 'guest_key' in request.session:
                p = request.session['guest_key']
                guest_cart = guestCart.objects.filter(user_ref=p)

                auth.login(request, user)
                for i in guest_cart:
                    try:
                        cart = Cart.objects.get(
                            user=request.user, product=i.product)
                        print(cart)
                    except:
                        cart = None
                    if cart:
                        print("one")
                        Cart.objects.filter(user=request.user, product=i.product).update(
                            quantity=cart.quantity+i.quantity)
                    else:
                        print("two")
                        k = Cart(user=request.user, product=i.product,
                                 quantity=i.quantity)
                        k.save()
                print("deleting guest cart")
                guest_cart.delete()
            messages.error(request, 'Account created')
            return redirect('user_login')
        else:
            messages.error(request, 'Otp not matching')
            return render(request, 'number_otp_verify.html', {'new_full_name': new_full_name, 'new_username': new_username, 'new_email': new_email,
                                                              'new_phone_number': new_phone_number, 'new_password2': new_password2})

    return render(request, 'number_otp_verify.html')


def otp_resend(request, new_phone_number):
    otp = 123456
    message_handler = MessageHandler(new_phone_number, otp).sent_otp_on_phone()
    return redirect('number_otp_verify')


@never_cache
def logout(request):
    auth.logout(request)
    return redirect('/')


def products(request):

    categori = Category.objects.all()
    price = request.GET.get('price', "")
    if 'search' in request.GET:
        search = request.GET['search']
        multiple_search = Q(Q(product_name__icontains=search)
                            | Q(chain__icontains=search))
        product = Products.objects.filter(multiple_search)

    else:
        product = Products.objects.all()
        categori = Category.objects.all()

    if request.user.is_authenticated:
        if price:
            product = product.filter(price__lt=price).order_by(('-price'))

        user = request.user
        cart_count = Cart.objects.filter(user=user).count()
        watchlist = Watchlist.objects.filter(user=request.user)
        watchlistItems = []
        for i in watchlist:
            watchlistItems.append(i.product)
    else:
        watchlist = {}
        watchlistItems = {}
        cart_count = {}
    context = {
        'products': product,
        'watchlistItems': watchlistItems,
        'category': categori,
        'cart_count': cart_count
    }
    return render(request, "products.html", context)


def categoryview(request, category_name):

    price = request.GET.get('price', "")
    category = get_object_or_404(Category, category_name=category_name)
    product = Products.objects.filter(category=category)

    if price:
        product = product.filter(price__lt=price).order_by(('-price'))

    return render(request, "category.html", {'product': product, 'category': category})


def product_details(request, id):

    product = Products.objects.get(id=id)
    productss = Products.objects.all()
    categori = Category.objects.all()

    if request.user.is_authenticated:
        user = request.user
        cart_count = Cart.objects.filter(user=user).count()
    else:
        cart_count = {}
    return render(request, 'product_details.html', {'product': product, 'products': productss, 'category': categori, 'cart_count': cart_count})


def my_profile(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).all()
        oldcart = OldCart.objects.filter(user=request.user).all()
        oldCart = reversed(list(oldcart))
        return render(request, 'my_profile.html', {'orders': orders, 'oldcart': oldCart})
    return redirect('user_login')


def wallet(request):
    if request.user.is_authenticated and request.user.is_active:
        balance = Wallet.objects.filter(user=request.user)

        return render(request, 'wallet.html', {'balance': balance})

    return redirect('user_login')


def my_products(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).all()
        # oldcart=OldCart.objects.filter(user = request.user).all()
        # oldCart = reversed(list(oldcart))

        return render(request, 'my_products.html', {'orders': orders})
    return redirect('user_login')


@never_cache
def edit_my_product(request, id):
    if request.user.is_authenticated and request.user.is_active:

        product = Products.objects.get(id=id)

        if request.method == 'POST':
            price = request.POST['price']
            product.price = price
            product.save()
            return redirect(my_products)
        return render(request, 'edit_my_product.html', {'product': product})
    return redirect('user_login')


def product_dont_Sell(request, id):
    if request.user.is_authenticated:
        product = Products.objects.get(id=id)
        product.is_active = False
        product.reselled = True
        product.save()
        return redirect('my_products')
    return redirect('user_login')


def product_resell(request, id):
    if request.user.is_authenticated:

        product = Products.objects.get(id=id)
        product.is_active = True
        product.reselled = False
        product.save()
        # order= Order.objects.get(id=id)
        # order.soldout=True
        # order.save()
        return redirect('my_products')
    return redirect('user_login')


def edit_profile(request, id):
    if request.user.is_authenticated:

        newUser = User.objects.get(id=id)

        if request.method == 'POST':
            username = request.POST['username']
            name = request.POST['full_name']
            email = request.POST['email']
            phone = request.POST['phone']

            newUser.username = username
            newUser.full_name = name
            newUser.email = email
            newUser.phone_number = phone
            newUser.save()
            return redirect('my_profile')
        return render(request, 'edit_profile.html', {'user_list': newUser})

    else:
        return redirect('user_login')


def changePassword(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(id=id)
            old = request.POST['old']
            new = request.POST['new']
            confirm = request.POST['confirm']

            if new != confirm:
                messages.info(request, "New Passwords aren't matching")
                return render(request, 'changepassword.html')

            elif not user.check_password(old):
                messages.info(request, "Wrong Old Password")
                return render(request, 'changepassword.html')
            else:
                user.set_password(new)
                user.save()
                messages.info(request, "Passsword changed Successfully:)")
                return redirect(my_profile)
        return render(request, 'changepassword.html')
    return redirect('user_login')


# pip install reportlab==3.6.6 => since getstring io error occured

def invoice_generate(request, id):
    oldcart = OldCart.objects.get(order_id=id)

    user = request.user
    template_path = 'invoice.html'
    print(oldcart.product.price)

    context = {'oldcart': oldcart, 'user': user}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="invoice.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def withdraw_wallet(request):
    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        withdraw = Wallet.objects.get(user=request.user)

        if withdraw.wall_amount < 300:
            messages.error(request, "Insuffient amount to withdraw")
            return redirect(wallet)
        else:
            withdraw.wall_amount = 0
            withdraw.save()
            return redirect(wallet)
    return redirect('user_login')
