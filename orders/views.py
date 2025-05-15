from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem, Cart
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def payments(request):
    if request.method == "POST":
        try:
            if not request.body:
                return JsonResponse({'error': 'No data received'}, status=400)

            body = json.loads(request.body)
            order = Order.objects.get(order_number=body['orderID'])

            if order.is_ordered:
                return JsonResponse({'message': 'La orden ya fue procesada'}, status=200)

            payment = Payment(
                payment_id=body['transID'],
                payment_method=body['payment_method'],
                amount_id=order.order_total,
                status=body['status'],
            )
            if request.user.is_authenticated:
                payment.user = request.user
            payment.save()

            order.payment = payment
            order.is_ordered = True
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart = Cart.objects.get(cart_id=request.session.session_key)
                cart_items = CartItem.objects.filter(cart=cart)

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order = order
                orderproduct.payment = payment
                if request.user.is_authenticated:
                    orderproduct.user = request.user
                orderproduct.product = item.product
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                orderproduct.variation.set(item.variation.all())
                orderproduct.save()

                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            cart_items.delete()

            mail_subject = 'Tu compra fue realizada!'
            email_body = render_to_string('orders/order_recieved_email.html', {
                'user': request.user.first_name if request.user.is_authenticated else order.first_name,
                'order': order,
            })

            to_email = request.user.email if request.user.is_authenticated else order.email
            send_email = EmailMessage(mail_subject, email_body, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()

            return JsonResponse({
                'order_number': order.order_number,
                'transID': payment.payment_id,
                'message': 'Compra exitosa'
            })

        except Order.DoesNotExist:
            print("❌ Error: Orden no encontrada.")
            return JsonResponse({'error': 'Orden no encontrada'}, status=404)

        except Exception as e:
            print("❌ Error en payments:", e)
            return JsonResponse({'error': str(e)}, status=500)


def place_order(request, total=0, quantity=0):
    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        try:
            cart = Cart.objects.get(cart_id=request.session.session_key)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_items = []

    if not cart_items or not cart_items.exists():
        return redirect('store')

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = round((16 / 100) * total, 2)
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()

            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            return render(request, 'orders/payments.html', {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            })
        else:
            return redirect('checkout')
    return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = sum(item.product_price * item.quantity for item in ordered_products)
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }

        return render(request, 'orders/order_complete.html', context)

    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')
