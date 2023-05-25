from django.db import models
from account.models import User
from payment.models import Payment
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True,auto_created=True)
    updated = models.DateTimeField(auto_now=True,auto_created=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    image = models.ImageField(null=True,blank=True)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=100, blank=True)
    price = models.IntegerField()
    availale = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,auto_created=True)
    updated = models.DateTimeField(auto_now=True,auto_created=True)    

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,)    
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True,auto_created=True)

    def __str__(self):
        return str(self.id)

class Status(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created = models.DateTimeField(auto_now_add=True,auto_created=True)
    updated = models.DateTimeField(auto_now=True,auto_created=True)

    def __str__(self):
        return self.name  

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    class type(models.TextChoices):
        on_delivery = 'on_delivery'
        online_payment = 'online_payment'
    payment_type = models.CharField(choices=type.choices, default='on_delivery', max_length=50, blank=True)
    payment_detail = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, blank=True,null=True)
    delivery_place = models.CharField(max_length=255, blank=True)
    total_payment = models.IntegerField(default=0,blank=True)
    total_quantity = models.IntegerField(default=0,blank=True)    
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,auto_created=True)
    updated = models.DateTimeField(auto_now=True,auto_created=True)
    def __str__(self):
        return str(self.id)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING,)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, null=True)
    status = models.ForeignKey(Status, blank=True, on_delete=models.DO_NOTHING, default=1)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=100,)
    description = models.TextField()
    status = models.CharField(max_length=10, default="open")
    type = models.CharField(max_length=40, default="others")
    created = models.DateTimeField(auto_now_add=True,auto_created=True)
    updated = models.DateTimeField(auto_now=True,auto_created=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class TicketDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True,auto_created=True)
    updated = models.DateTimeField(auto_now=True,auto_created=True)

    def __str__(self):
        return str(self.id)