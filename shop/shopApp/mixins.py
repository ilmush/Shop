from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import Category, Customer, Cart, Product


class CategoryDetailMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_products'] = Product.objects.filter(category=self.object.id)
        return context


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
