from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.decorators.cache import never_cache
from .models import *
from django.contrib.auth import get_user_model
from accounts.models import *
User = get_user_model()

# create your view here


def cart(request):

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart_count = Cart.objects.filter(user=user).count()

        if len(cart) == 0:
            return render(request, 'cart.html', {'cart_count': cart_count})
        else:

            subtotal = 0
            for i in cart:
                x = i.product.price
                subtotal = subtotal+x
            total = subtotal
            return render(request, 'cart.html', {'cart': cart, 'subtotal': subtotal, 'total': total, 'cart_count': cart_count})

    else:
        if not request.session.session_key:
            request.session.create()
        request.session['guest_key'] = request.session.session_key
        key = request.session['guest_key']
        cart = guestCart.objects.filter(user_ref=request.session.session_key)
        cart_count = guestCart.objects.filter(
            user_ref=request.session.session_key).count()
        subtotal = 0
        for i in cart:
            x = i.product.price
            subtotal = subtotal+x
        offer = 0
        total = subtotal + offer
        return render(request, 'cart.html', {'cart': cart, 'subtotal': subtotal, 'total': total, 'cart_count': cart_count})


def addTocart(request, id):

    if request.user.is_authenticated and request.user.is_active:
        product = Products.objects.get(id=id)
        uid = request.user
        if Cart.objects.filter(product=id, user=uid).exists():
            cart = Cart.objects.get(product=id, user=uid)
            cart.save()
            return redirect('products')
        else:
            cart = Cart.objects.create(product=product, user=uid)
            return redirect('products')
    else:
        if not request.session.session_key:
            request.session.create()
        product = Products.objects.get(id=id)
        uid = request.user
        if guestCart.objects.filter(product=id, user_ref=request.session.session_key).exists():
            cart = guestCart.objects.get(product=id, user=uid)
            cart.save()
            return redirect('products')
        else:
            cart = guestCart.objects.create(
                product=product, user_ref=request.session.session_key)
            return redirect('products')


def removecart(request, id):
    if request.user.is_authenticated and request.user.is_active:
        cart = Cart.objects.get(id=id)
        cart.delete()
        messages.error(request, "Item removed")
        return redirect("cart")
    else:
        cart = guestCart.objects.get(id=id)
        cart.delete()
        messages.error(request, "Item removed")
        return redirect("cart")


def checkout(request):

    if request.user.is_authenticated and request.user.is_active:

        balance = Wallet.objects.filter(user=request.user)
        cart = Cart.objects.filter(user=request.user)
        subtotal = 0
        for i in cart:
            x = i.product.price
            subtotal = subtotal+x
            total = subtotal

        if request.method == 'POST':
            payment = request.POST['payment_selector']
            user = request.user
            cart = Cart.objects.filter(user=request.user)
            subtotal = 0
            for i in cart:
                x = i.product.price
                subtotal = subtotal+x
            total = subtotal

            for i in cart:
                order = Order.objects.create(
                    user=user, amount=total, method=payment, product=i.product)
                order.save()
                oldcart = OldCart.objects.create(
                    user=user, product=i.product, order=order, total=total)
                oldcart.save()
                product = Products.objects.get(id=i.product_id)
                product.old_owner = product.new_owner
                product.new_owner = request.user.username
                product.is_active = False
                product.reselled = True
                product.save()
                print("product saved")

            cart.delete()
            messages.error(request, "Order Placed")
            return redirect('cart')

        return render(request, 'checkout.html', {'subtotal': subtotal, 'total': total, 'balance': balance})
    else:
        return redirect('user_login')


def paywith_wallet(request):

    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        cart = Cart.objects.filter(user=request.user)
        wallet = Wallet.objects.get(user=request.user)
        subtotal = 0

        for i in cart:
            x = i.product.price
            subtotal = subtotal+x
        total = subtotal

        if total > wallet.wall_amount:
            messages.error(request, 'insufficient balance')
            return redirect('checkout')
        elif total <= wallet.wall_amount:
            wallet.wall_amount = wallet.wall_amount-total
            wallet.save()
            for i in cart:
                order = Order.objects.create(
                    user=user, amount=total, product=i.product)
                order.save()
                oldcart = OldCart.objects.create(
                    user=user, product=i.product, order=order, total=total)
                oldcart.save()
                product = Products.objects.get(id=i.product_id)
                product.old_owner = product.new_owner
                product.new_owner = request.user.username
                product.is_active = False
                product.reselled = True
                product.save()
            cart.delete()
            messages.error(request, "Order Placed")
            return redirect('my_profile')
        else:
            messages.error(request, 'somthing went wrong')
            return redirect('checkout')
    else:
        return redirect('user_login')


def watchlist(request):
    if request.user.is_authenticated:
        user = request.user
        watchlist = Watchlist.objects.filter(user=request.user)
        return render(request, 'watchlist.html', {'watchlist': watchlist})
    return redirect('user_login')


def addToWatchlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Products.objects.get(id=prod_id)
        user = request.user
        watchlist = Watchlist.objects.create(user=user, product=product)
        watchlist.save()


# remove by clicking heart button
def removeFromWatchlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Products.objects.get(id=prod_id)
        user = request.user
        watchlist = Watchlist.objects.filter(user=user, product=product)
        watchlist.delete()
        return JsonResponse({'status': True})

# remove by clicking normal button in wishlist page


def removeWatchlist(request, id):
    product = Products.objects.get(id=id)
    user = request.user
    watchlist = Watchlist.objects.filter(user=user, product=product)
    watchlist.delete()
    return redirect('watchlist')
