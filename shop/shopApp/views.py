from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, ListView

from .models import *
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm
from .utils import recalc_cart


class BaseView(CartMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'base.html'
    slug_url_kwarg = 'slug'
    paginate_by = 10
    categories = Category.objects.all()
    specifications = Specification.objects.all()
    extra_context = {
        'categories': categories,
        'specifications': specifications,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['related_products'] = Product.objects.order_by('-id')[:4]
        return context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
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
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        context = {
            'cart': self.cart,
            'category': category
        }
        return render(request, 'cart.html', context)


class OrderView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'category': category,
            'form': form
        }
        return render(request, 'order.html', context)


class MakeOrderView(CartView, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.delivery = form.cleaned_data['delivery']
            new_order.comment = form.cleaned_data['comment']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/order')
