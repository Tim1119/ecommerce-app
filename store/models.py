from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(default='placeholder.png',upload_to='product-images')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
       

    def __str__(self):
        return self.name 
    
    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered= models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return round(total,2)

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        quantity = sum([item.quantity for item in order_items])
        return quantity


    def __str__(self):
        return str(self.id) + str(self.transaction_id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_ordered= models.DateTimeField(auto_now_add=True)
   

    @property
    def get_total(self):
        total = float(self.product.price) * float(self.quantity)
        return total

    def __str__(self):
        return str(self.order) + str(self.product)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


    


    

