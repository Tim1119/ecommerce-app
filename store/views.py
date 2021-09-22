from django.db.models.query_utils import check_rel_lookup_compatibility
from django.shortcuts import render
from django.views.generic import ListView
from .models import Customer, Order, Product,OrderItem, ShippingAddress
from django.http import JsonResponse, request
import json,datetime
from .utils import cookieCart,cartData,guestOrder

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        data= cartData(self.request)
        cartItems =data['cartItems']
       

        context['products'] = Product.objects.all()
        context['cartItems'] = cartItems
        return context
       

class CartListView(ListView):
    model = Order
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data= cartData(self.request)
        cartItems =data['cartItems']
        order =data['order']
        items =data['items']

        context['cartItems'] = cartItems
        context['items'] = items
        context['order'] = order
            
        return context


class CheckoutListView(ListView):
   model = Order
   template_name = 'store/checkout.html'
   
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data= cartData(self.request)
        cartItems =data['cartItems']
        order =data['order']
        items =data['items']

        context['cartItems'] = cartItems
        context['items'] = items
        context['order'] = order
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

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer 
        order,created= Order.objects.get_or_create(customer,complete=False)
       
    else:
        customer,order = guestOrder(request,data)
       
        total=float(data['form']['total'])
        order.transaction_id = transaction_id  

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer = customer,
            order =order,
            address = data['shipping']['address'],
            city =  data['shipping']['city'],
            state =  data['shipping']['state'],
            zipcode =  data['shipping']['zipcode'],
        )


    return JsonResponse('Payment Complete',safe=False)

    