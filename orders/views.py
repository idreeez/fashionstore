from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import Cart
from django.utils import timezone
from .models import Coupon
from django.contrib import messages 

def create_order(request):
    cart_items = Cart.objects.filter(session_key=request.session.session_key)

    if not cart_items.exists():
        messages.warning(request, "Ваша корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect('cart:cart')

    subtotal = sum(Decimal(item.total_price()) for item in cart_items)

    # Обработка купона
    coupon_id = request.session.get('coupon_id')
    discount_amount = Decimal('0.00')
    total = subtotal

    if coupon_id:
        try:
            coupon = Coupon.objects.get(
                id=coupon_id,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            discount_amount = (subtotal * Decimal(coupon.discount) / Decimal('100')).quantize(Decimal('0.01'))
            total = (subtotal - discount_amount).quantize(Decimal('0.01'))
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
            request.session.pop('discount_amount', None)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.session_key = request.session.session_key
            order.subtotal = subtotal
            order.discount_amount = discount_amount
            order.total = total
            order.save()

            # Очистка корзины и купонов
            cart_items.delete()
            request.session.pop('discount_amount', None)
            request.session.pop('coupon_id', None)

            return redirect('orders:order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'orders/create.html', {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'total': total
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})
