from django.shortcuts import render
from django.views.generic import DetailView
from .models import Milk, Drinks, Home


def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):

    # построение соответсвий между имнами моделей и самими моделями
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
