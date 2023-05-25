from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.views import View
from food.models import Item,Category,Cart,Order,OrderDetail
from .models import Payment
from .payment import Pay,Checkout,CheckPayment
# Create your views here.

class Payment(View):
    def get(self,request,id):
        order = get_object_or_404(Order,id=id)
        if order.payment_type == 'on_delivery':
            return redirect('orders')            
        else:
            print(order)
            check = CheckPayment(order)
            if check == 'success':
                return redirect('home')
            else:
                order_count = Order.objects.filter(user=request.user).count()            
                cart_count = Cart.objects.filter(user=request.user).count()
                url = order.payment_detail.reference_url
                context = {'cart_count':cart_count,'order_count':order_count,'url':url}
                return render(request,'payment/pay.html', context)
