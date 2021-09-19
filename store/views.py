from django.http.response import HttpResponse
from store.models import Product
from django.shortcuts import render
from django.views.generic import ListView
from .models import Order, Product,OrderItem
from django.http import JsonResponse
import json
from .models import Order,OrderItem

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order,created = Order.objects.get_or_create(customer=customer,complete=False)
            items= order.orderitem_set.all()
            cartItems = order.get_cart_items
            context['items'] = items
            context['order'] = order
            context['cartItems'] = cartItems
            return context
        else:
            order = {'get_cart_items':0,'get_cart_total':0}
            cartItems = order['get_cart_items']
            context['items'] = []
            context['order'] = order
            context['cartItems'] = cartItems
            
            return context 

class CartListView(ListView):
    model = Order
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order,created = Order.objects.get_or_create(customer=customer,complete=False)
            items= order.orderitem_set.all()
            cartItems = order.get_cart_items
            context['items'] = items
            context['order'] = order
            context['cartItems'] = cartItems
            return context
        else:
            order = {'get_cart_items':0,'get_cart_total':0}
            context['items'] = []
            context['order'] = order
            context['cartItems'] = order['get_cart_items']
            return context


class CheckoutListView(ListView):
   model = Order
   template_name = 'store/checkout.html'
   
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order,created = Order.objects.get_or_create(customer=customer,complete=False)
            items= order.orderitem_set.all()
            context['items'] = items
            context['order'] = order
            context['cartItems'] = order.get_cart_items
            return context
        else:
            order = {'get_cart_items':0,'get_cart_total':0}
            context['items'] = []
            context['order'] = order
            context['cartItems'] = order['get_cart_items']
            return context

def homeview(request):
    return render(request,'store/store.html')
from django.core import serializers 


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)
    