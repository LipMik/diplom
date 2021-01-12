from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse  # построение урла для объекта


#Categorys +

#Product +
#Milk  +
#Drinks +
#FullList +

#Cart +
#CartPlast +
#CartPaper +
#CartGlas +
#CartGeneral +
#CartDanger +

#Customer +


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    code = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Код переработки')
    code_2 = models.CharField(max_length=10, verbose_name='Код переработки(буквенный)')
    period = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Период разложения (лет)')
    weight = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Вес отходов (кг)')
    name = models.CharField(max_length=255, verbose_name='Наимаенование продукта')
    result = models.CharField(max_length=255, verbose_name='Результат разложения')

    def __str__(self):
        return self.title


class FullList(Product):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Milk(Product):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Drinks(Product):

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):
    # промежуточная корзина

    user = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_weight = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общий вес отходов')

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_weight = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общий вес отходов')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartPlast(models.Model):

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.OneToOneField(Cart, blank=True, related_name='related_plast', on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)

    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartPaper(models.Model):

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.OneToOneField(Cart, blank=True, related_name='related_paper', on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartGlas(models.Model):

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.OneToOneField(Cart, blank=True, related_name='related_glas', on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartGeneral(models.Model):

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.OneToOneField(Cart, blank=True, related_name='related_general', on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartDanger(models.Model):

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.OneToOneField(Cart, blank=True, related_name='related_danger', on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    adress = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)