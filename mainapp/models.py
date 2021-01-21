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


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        product = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('product_code')[:5]
            product.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        product, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                        reverse=True
                    )
        return product


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    category_name = {
        'Молочные продукты': 'milk__count',
        'Напитки': 'drinks__count',
        'Бытовые товары': 'home__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_bar(self):
        model = get_models_for_count('milk', 'drinks', 'home')
        qs = list(self.get_queryset().annotate(*model))
        data = [dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.category_name[c.name])) for c in qs]
        return data


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    # построение универсальных урлов для всех продуктов

    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Вес отходов (кг)')
    product_code = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.title

    # for delete from cart
    def get_model_name(self):
        return self.__class__.__name__.lower()


class FullList(models.Model):

    title = models.CharField(max_length=255, verbose_name='Расшифровка кода')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    period = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Период разложения (лет)')
    result = models.CharField(max_length=255, verbose_name='Результат разложения')
    code = models.CharField(max_length=3, verbose_name='Числовой код переработки')
    mark = models.BooleanField(default=True, verbose_name='Возможность вторичной переработки')
    result_cart_number = models.IntegerField(verbose_name='Номер урны', default=5)

    def __str__(self):
        return "{} : {}".format(self.code, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Milk(Product):

    code = models.ForeignKey(FullList, verbose_name='Код переработки', on_delete=models.CASCADE)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Drinks(Product):
    code = models.ForeignKey(FullList, verbose_name='Код переработки', on_delete=models.CASCADE)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Home(Product):
    code = models.ForeignKey(FullList, verbose_name='Код переработки', on_delete=models.CASCADE)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    # промежуточное состояние товара, добавляется в корзину не сам товар, а content_object

    user = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_weight = models.DecimalField(max_digits=9, decimal_places=2, default=0.1, verbose_name='Общий вес отходов')

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_weight = self.qty * self.content_object.weight
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    final_weight = models.DecimalField(max_digits=9, decimal_places=2, default=0.1, verbose_name='Общий вес отходов')

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     cart_data = self.products.aggregate(models.Sum('final_weight'), models.Count('id'))
    #     # print(cart_data)
    #
    #     if cart_data.get('final_weight__sum'):
    #         self.final_weight = cart_data['final_weight__sum']
    #     else:
    #         self.final_weight = 0
    #     self.total_products = cart_data['id__count']
    #     super().save(*args, **kwargs)


class CartPlast(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_plast')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartPaper(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_paper')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartGlas(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_glas')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartGeneral(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_general')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartDanger(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_danger')
    total_products = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
