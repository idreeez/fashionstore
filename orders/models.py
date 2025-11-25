from django.db import models
from decimal import Decimal
from products.models import Product 
from cart.models import Coupon

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # Теперь Product определен
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def get_cost(self):
        return (self.price or Decimal("0.00")) * (self.quantity or 0)




class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен')
    ]
    
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    address = models.TextField("Адрес")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True)
    
    # Финансовые поля
    subtotal = models.DecimalField("Сумма без скидки", max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField("Скидка", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField("Итого", max_digits=10, decimal_places=2)
    
    coupon = models.ForeignKey(
        Coupon,
        verbose_name="Купон",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.items.exists() and hasattr(self, 'session_key'):
            from cart.models import Cart  # Локальный импорт для избежания циклических зависимостей
            cart_items = Cart.objects.filter(session_key=self.session_key)
            for item in cart_items:
                OrderItem.objects.create(
                    order=self,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart_items.delete()