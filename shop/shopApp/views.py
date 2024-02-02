from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView

from .models import *
from .mixins import CategoryDetailMixin, CartMixin


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        products = Product.objects.all()
        context = {
            'category': category,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'base.html', context)


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        context = {
            'cart': self.cart,
            'category': category
        }
        return render(request, 'cart.html', context)
