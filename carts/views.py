# carts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm  # Importa el formulario aquí

# ===================== FUNCIONES AUXILIARES =====================
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# ===================== VISTAS PRINCIPALES =====================
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    product_variation = []
    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except:
                pass

    if current_user.is_authenticated:
        cart_item_qs = CartItem.objects.filter(product=product, user=current_user)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item_qs = CartItem.objects.filter(product=product, cart=cart)

    for item in cart_item_qs:
        if list(item.variation.all()) == product_variation:
            item.quantity += 1
            item.save()
            break
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=current_user if current_user.is_authenticated else None,
            cart=None if current_user.is_authenticated else cart
        )
        if product_variation:
            cart_item.variation.set(product_variation)
        cart_item.save()

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = round((16 / 100) * total, 2)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = round((16 / 100) * total, 2)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    form = OrderForm()
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'form': form
    }
    return render(request, 'store/checkout.html', context)
