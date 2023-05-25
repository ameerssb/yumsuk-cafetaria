from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.contrib import messages
from .models import Item,Category,Cart,Status,Order,OrderDetail
from payment.models import Payment
from .forms import CartForm,OrderForm,OrderDetailsForm
from payment.payment import Pay
# Create your views here.

general = [login_required]

@method_decorator(general,name='post')
class Home(View):
    def get(self,request):
        if request.GET.get('search'):
            category = Category.objects.all().order_by('created').values()            
            if not request.GET.get('search') == "__":
                search = request.GET.get('search')
                items = Item.objects.filter(name__icontains=search,availale=True).order_by('created').values()
                data = {'resp':list(items),'category':list(category)}
                return JsonResponse(data)
            else:
                items = Item.objects.filter(availale=True).order_by('created').values()
                data = {'resp':list(items),'category':list(category)}
                return JsonResponse(data)
        else:
            a = []
            category = Category.objects.all().order_by('created')
            for i in category:
                b = []
                b.append(i.name)
                b.append(Item.objects.filter(category=i.id,availale=True).order_by('created'))
                a.append(b)
            context = {'categories':category,'values':a,}
            return render(request, 'food/index.html', context)

    def post(self,request):
        return redirect('home')

@method_decorator(general,name='get')
@method_decorator(general,name='post')
class Carts(View):
    def get(self,request):
        order_count = Order.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user).count()        
        cart = Cart.objects.filter(user=request.user)
        if request.GET.get('item'):
            item = request.GET.get('item')
            cart = Cart.objects.get(user=request.user,id=item)          
            price = int(cart.item.price) * int(cart.quantity)
            data = {'resp':price}
            return JsonResponse(data)            
        context = {'cartItems':cart,'cart_count':cart_count,'order_count':order_count,}
        return render(request,'food/cart.html',context)
    def post(self,request):
        cc = Cart.objects.filter(user=request.user,item=request.POST['item']).first()
        c = CartForm(instance=cc)
        if c.instance.pk == None:
            data = CartForm(request.POST or None)
            if data.is_valid():
                cart = data.save(commit=False)
                cart.user = request.user
                cart.save()
                cart = Cart.objects.filter(user=request.user).count()
                m = "Items added to cart Successfully"
                data = {'message':m,'cart':cart}
                return JsonResponse(data)
            else:
                m = "an error occured while adding to cart please try again"
                data = {'message':m}
                return JsonResponse(data)            
        else:
            cc.quantity += int(request.POST['quantity'])
            cc.save()
            cart_count = Cart.objects.filter(user=request.user).count()
            m = "Items added to cart Successfully"
            data = {'message':m,'cart_count':cart_count}
            return JsonResponse(data)

@method_decorator(general,name='get')
@method_decorator(general,name='post')
class Orders(View):
    def get(self,request,id,quantity=None):
        order_count = Order.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user).count()                    
        if quantity == None:
            cart_id = id
            cart = Cart.objects.get(user=request.user,id=cart_id)
            price = int(cart.item.price) * int(cart.quantity)
            # order_detail = OrderDetailsForm(request.POST)
            context = {'item':cart.item,'quantity':cart.quantity,'price':price,'cart_count':cart_count,'order_count':order_count,}
            return render(request,'food/order.html',context)
        else:
            quick_id = id
            quantity = quantity
            quick = Item.objects.get(id=quick_id)
            price = int(quick.price) * int(quantity)
            context = {'item':quick,'quantity':quantity,'price':price,'cart_count':cart_count,'order_count':order_count,}
            return render(request,'food/order.html',context)
    def post(self,request,id,quantity=None):
        order = OrderForm(request.POST or None)
        order_detail = OrderDetailsForm(request.POST)
        if order.is_valid():
            order = order.save(commit=False)
            order.user = request.user
            if order_detail.is_valid():
                order_detail = order_detail.save(commit=False)
                order_detail.order = order
                order.total_payment = order_detail.price
                order.total_quantity = order_detail.quantity
                if request.POST['payment_type'] == "on_delivery":
                    order.save()
                    order_detail.save()
                    return redirect('orders')
                else:                    
                    payment = {'status':False}
                    try:
                        payment = Pay(str(request.user.email),order_detail.price)
                    except:
                        messages.error(request,"Check your Internet Connection or try again later.")
                        if quantity == None:
                            return redirect('cart_order',id)
                        else:
                            return redirect('quick_order',id,quantity)
                    if payment['status'] == False:
                        data = {'message':'Failed',}
                        messages.error(request,"An errored while initiating Online Payment. Try again or choose other method.")
                        if quantity == None:
                            return redirect('cart_order',id)
                        else:
                            return redirect('quick_order',id,quantity)
                    else:
                        data = Payment(reference_number = payment['data']['reference'],reference_url = payment['data']['authorization_url'])
                        data.save()
                        order.payment_detail = data
                        order.save()
                        order_detail.save()
                        return redirect(f'/payment/pay/{order.id}')
            else:
                messages.error(request,"An error occured, fill your order form correctly.")
                if quantity == None:
                    return redirect('cart_order',id)
                else:
                    return redirect('quick_order',id,quantity)
        else:
            messages.error(request,"An error occured, fill your order form correctly.")
            if quantity == None:
                return redirect('cart_order',id)
            else:
                return redirect('quick_order',id,quantity)

@method_decorator(general,name='get')
@method_decorator(general,name='post')
class Multi_Orders(View):
    def get(self,request,id,quantity):
        id = str(id).split('-')
        quantity = str(quantity).split('-')
        id.remove('')
        quantity.remove('')
        for i in range(len(quantity)):
            quantity[i] = int(quantity[i])
        order_count = Order.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user).count()            
        price = []
        orders = Item.objects.filter(id__in=id)
        for i in range(orders.count()):            
            price.append(int(orders[i].price) * int(quantity[i]))            

        all_list = zip(price,quantity,orders)
        context = {'orders':all_list,'orders_count':orders.count(),'order_price':sum(price),'order_quantity':sum(quantity),'cart_count':cart_count,'order_count':order_count,}            
        return render(request,'food/multi_order.html',context)
    def post(self,request,id,quantity):
        k = {}
        s = request.POST
        s = s.copy()
        s['item'] = s.getlist('item')
        s['quantity'] = s.getlist('quantity')
        s['price'] = s.getlist('price')
        s = s.dict()
        k = s.copy()
        order_details = {}
        for i in range(len(s['item'])):
            k['item'] = s['item'][i]
            k['price'] = s['price'][i]
            k['quantity'] = s['quantity'][i]            
            order_details[i] = OrderDetailsForm(k.copy())
            
        order = OrderForm(k)
        decision = func_decision(order_details)
        if decision == True and order.is_valid():
            order = order.save(commit=False)
            order.user = request.user
            for i in range(len(order_details)):
                order_detail = order_details[i]
                order_detail = order_detail.save(commit=False)
                order_detail.order = order                    
            order.total_payment = k['total_price']
            order.total_quantity = k['total_quantity']
            if request.POST['payment_type'] == "on_delivery":
                order.save()
                for i in range(len(order_details)):
                    order_detail = order_details[i]
                    order_detail.save()
                return redirect('orders')
            else:
                payment = {'status':False}
                try:
                    payment = Pay(str(request.user.email),order.total_payment)
                except:
                    messages.error(request,"Check your Internet Connection or try again later.")
                    return redirect('multi_order',id,quantity)
                if payment['status'] == False:
                    data = {'message':'Failed',}
                    messages.error(request,"An errored while initiating Online Payment. Try again or choose other method.")
                    return redirect('multi_order',id,quantity)
                else:
                    data = Payment(reference_number = payment['data']['reference'],reference_url = payment['data']['authorization_url'])
                    data.save()
                    order.payment_detail = data
                    order.save()
                    for i in range(len(order_details)):
                        order_detail = order_details[i]
                        order_detail.save()
                    return redirect('pay',order.id)
        else:
            messages.error(request,"An error occured, fill your order form correctly.")
            return redirect('multi_order',id,quantity)
        # return redirect(f'multi_order',id,quantity)

@method_decorator(general,name='get')
@method_decorator(general,name='post')
class All_Orders(View):
    def get(self,request):
        orders = Order.objects.filter(user=request.user).order_by('-created')
        order_details = OrderDetail.objects.filter(order__in=orders)
        order_count = Order.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user).count()
        all_list = order_details
        all_quantity = 0
        for i in all_list:
            all_quantity += i.quantity
        context = {'cart_count':cart_count,'order_count':order_count,'all_list':all_list,'all_quantity':all_quantity,'orders':orders}
        return render(request,'food/orders.html', context)
  
    def post(self,request):
        id = request.POST['cancel_order']
        detail = OrderDetail.objects.get(id=id)
        details = OrderDetail.objects.filter(order=detail.order)
        order = Order.objects.get(id=detail.order.id)

        if details.count() > 0:
            status = Status.objects.get(id=4)
            detail.status = status
            order.total_payment -= detail.price
            order.total_quantity -= detail.quantity
            detail.save()
            order.save()

        return redirect('orders')
        
        
def func_decision(order_details):
    decision = False    
    for o in range(len(order_details)):
        if order_details[o].is_valid():
            decision = True
        else:
            decision = False
            break
    return decision

# @login_required               
# def Cancel_Order(request):
#     if request.method == 'POST':
#         id = request.POST['order']
#         detail = OrderDetail.objects.get(id=id)
#         details = OrderDetail.objects.filter(order=detail.order)
#         order = Order.objects.get(id=detail.order)
        
#         if details.count() == 1:
#             order.delete()
#             detail.delete()
#         elif details.count() > 1:
#             order.total_payment -= detail.price
#             order.total_quantity -= detail.quantity
#             detail.delete()
            
@login_required
def count(request):
    if request.method == 'GET':
        order_count = Order.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user).count()    
        data = {'order_count':order_count,'cart_count':cart_count}
        return JsonResponse(data)    

@login_required          
def Cart_Remove(request):
    if request.method == 'POST':
        id = request.POST['cart']
        cart = Cart.objects.filter(user=request.user,id=id)
        if cart.count() == 1:
            cart.first().delete()
            cart = Cart.objects.all().count()
            data = {'cart':cart,'m': "Deleted Successfully",'status':200}
            return JsonResponse(data)
        else:
            data = {'m': "Can't Delete this cart or is not available",'status':404}
            return JsonResponse(data)