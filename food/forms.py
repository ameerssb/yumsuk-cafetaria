from django.forms import ModelForm
from .models import Cart,Order,OrderDetail,Item

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ('item','quantity',)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user','payment_detail',)
    
class OrderDetailsForm(ModelForm):
    class Meta:
        model = OrderDetail
        exclude = ('order','status',)
        