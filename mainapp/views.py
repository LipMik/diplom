from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from .models import Milk, Drinks, Home, Category, LatestProducts, Customer, Cart, CartProduct, FullList, CartGlas, CartPlast, CartPaper, CartGeneral, CartDanger
from .mixins import CategoryDetailMixin, CartMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_bar()
        products = LatestProducts.objects.get_products_for_main_page('home', 'drinks', 'milk', with_respect_to='milk')
        test_dict = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'base.html', test_dict)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    # построение соответсвий между именами моделей и самими моделями
    CT_MODEL_MODEL_CLASS = {
        'milk': Milk,
        'drinks': Drinks,
        'home': Home
    }

    # переопределение стандарного dispatch метода
    def dispatch(self, request, *args, **kwargs):

        # получение из словаря по ключу модели
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    # для категорий
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):

    # для корзины
    def get(self, request, *args, **kwargs):

        categories = Category.objects.get_categories_for_left_bar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class AddProduct(CartMixin, View):

    def get(self, request, *args, **kwargs):
        # print(kwargs.get('ct_model'))
        # print(kwargs.get('slug'))
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)  # получить продукт

        product = content_type.model_class().objects.get(slug=product_slug)

        cart_product, created = CartProduct.objects.get_or_create(user=self.cart.owner, cart=self.cart,
                                                                  content_type=content_type,
                                                                  object_id=product.product_code
                                                                  )
        if created:
            self.cart.products.add(cart_product)
        messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
        # recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')
        # удаление товара
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                                                  content_type=content_type,
                                                                  object_id=product.product_code)
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар удален из корзины')
        return HttpResponseRedirect('/cart/')


class ChangeQTY(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')
        # добавление товара
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart,
                                               content_type=content_type,
                                               object_id=product.product_code)
        qty = int(request.POST.get('qty'))
        # print(request.POST)
        cart_product.qty = qty
        cart_product.save()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Количество товара изменено')
        return HttpResponseRedirect('/cart/')


class SortView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_bar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'sort.html', context)

# get_or_create возвращает tuple

        # print(product.code_id)
        # answer = FullList.objects.get(id=product.code_id)
        # print(answer)
        # cart_type_number = answer.result_cart_number
        # print(answer)
        # print('номер урны:', cart_type_number)
        # print(answer.slug) +

# def sort_trash(self,c_n,customer):
#
#         # выбор итоговой корзины
#
#     if c_n == 1:
#         print('Пластик')
#         cart, created = CartPlast.objects.get_or_create(owner=customer, in_order=False)
#         cart_product = CartPlast.objects.create(owner=cart.owner)
#         print(cart_product)
#         print(created)
#
#     # elif c_n == 2:
#     #     cart_product, created = CartPaper.objects.get_or_create(owner=cart.owner)
#     #     print(created)
#     #     print('Бумага')
#     # elif c_n == 3:
#     #     cart_product, created = CartGlas.objects.get_or_create(owner=cart.owner)
#     #     print(created)
#     #     print('Стекло')
#     elif c_n == 4:
#         cart, created = CartDanger.objects.get_or_create(owner=customer, in_order=False)
#         cart_product = CartDanger.objects.create(owner=cart.owner)
#         print(created)
#         print('Опасный')
#     # else:
#     #     print('Общий мусор')
#     #     cart_product, created = CartGeneral.objects.get_or_create(owner=cart.owner)
#     #     print(created)