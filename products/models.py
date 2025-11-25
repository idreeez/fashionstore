from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to='products/')
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    available = models.BooleanField("В наличии", default=True)
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name