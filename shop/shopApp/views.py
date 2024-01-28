from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import *
from .mixins import CategoryDetailMixin


class BaseView(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        products = Product.objects.all()
        context = {
            'category': category,
            'products': products
        }
        return render(request, 'base.html', context)


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class ProductDetailView(CategoryDetailMixin, DetailView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
