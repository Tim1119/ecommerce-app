from django.db.models.query_utils import check_rel_lookup_compatibility
from django.shortcuts import render
from django.views.generic import ListView
from .models import Customer, Order, Product,OrderItem, ShippingAddress
from django.http import JsonResponse, request
import json,datetime


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
            order = {'get_cart_items':0,'get_cart_total':0,'shipping':False}
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
            try:
                cart =json.loads(self.request.COOKIES['cart'])
                print(cart)
            except:
                cart={}
            
            order = {'get_cart_items':0,'get_cart_total':0,'shipping':False}
            
            
            cartItems= order['get_cart_items']

            for i in cart:
                cartItems +=cart[i]['quantity']
                
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                order['get_cart_total']+=total 
                order['get_cart_items']+=cart[i]['quantity']
                item={
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL
                    },
                    'quantity':cart[i] ['quantity'],
                    'get_total':total,
                }
                items =[].append(item)


            context['cartItems'] = cartItems
            context['items'] = items
            context['order'] = order
            
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
            order = {'get_cart_items':0,'get_cart_total':0,'shipping':False}
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

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer 
        order,created= Order.objects.get_or_create(customer,complete=False)
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

    else:
        print('user is not logged in')
    return JsonResponse('Payment Complete',safe=False)

    