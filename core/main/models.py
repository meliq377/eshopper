from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['id']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Brand(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['id']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name='Url', unique=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    img = models.ImageField(upload_to='media')
    web_id = models.CharField(max_length=100)
    availability = models.CharField(max_length=100, choices=(('In Stock', 'In Stock'),
                                                             ('In not Stock', 'In not Stock')))
    condition = models.CharField(max_length=100, blank=True, choices=(('New', 'New'),
                                                                      ('Sale', 'Sale')))
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-id']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([item.get_total for item in orderproducts])
        return total

    @property
    def get_itemtotal(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([item.quantity for item in orderproducts])
        return total

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    @property
    def get_cart_all_total(self):
        total = self.get_cart_total + 2
        return total


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'orderproduct'
        verbose_name_plural = 'orederproducts'
        ordering = ['user_id']
