import os
from .models import Payment
from paystackapi.paystack import Paystack
paystack_secret_key = str(os.environ.get('PAYSTACK'))
paystack_secret_key = 'sk_test_afb5899f3131f1b6aaa3bdcbf698550cc478de5c'
paystack = Paystack(secret_key=paystack_secret_key)

# Create your views here.

def Pay(email,amount):
    amount = int(amount) * 100
    payment = paystack.transaction.initialize(email=email,amount=amount)
    return payment

def Checkout(reference):
    try:
        status = paystack.transaction.verify(reference)
    except:
        status = {'status': False, 'data':{'status': 'failed'}}
    if status['status'] == True:
        if status['data']['status'] == 'success':
            return 'success'
        else:
            return 'unpaid'
    else:
        return 'failed'

def CheckPayment(data):    
    check = Checkout(data.payment_detail.reference_number)
    if check == 'success':
        update = Payment.objects.get(id=data.payment_detail.id)
        update.payment = 'Paid'
        update.save()
    else:
        if data.payment_detail.payment != 'Unpaid':
            update = Payment.objects.get(id=data.payment_detail.id)
            update.payment = 'Unpaid'
            update.save()
    return check