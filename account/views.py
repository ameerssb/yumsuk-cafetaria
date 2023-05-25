from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect,get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from verify_email.email_handler import send_verification_email
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
# from question.models import Question, Answer
from .forms import VerifyForm, Update, CreateUserForm
from food.models import Cart,Order
from .models import User

#from . import verify



signout_deco = [login_required]

class Signin(View):
    def get(self,request):        
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = CreateUserForm()
            context = {'form':form,}

            return render(request, 'account/signin.html', context)

    def post(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            if request.POST['type'] == 'register':
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    try:
                        data = form.save(commit=False)
                        data.is_email_verified = False
                        data.save()
                        # send_verification_email(request, data)
                        messages.success(request, "Account created, You can login now")
                        return redirect('Signin')
                    except:
                        messages.error(request, "Account not created! an error occured  please try again or contact us at customer support")
                        return redirect('Signin')
                else:
                    messages.error(request, "The Registration form contains an error please fill it correctly")
                    return redirect('Signin')                        
                
            elif request.POST['type'] == 'login':
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)
                u = User.objects.filter(email=email).first()
                if user is not None:
                    if user.is_active:
                        # if u.is_email_verified:
                        login(request, user)
                        if request.GET.get('next'):
                            return redirect(request.GET.get('next'))
                        else:  
                            return redirect('home')
                        # else:
                        #   messages.error(request,"Your email is not verified, Please verify before Signing in")
                        #   return redirect('Signin')                    
                    else:
                        messages.error(request,"Your account is disabled, Contact Us via Suppport Team")
                        return redirect('Signin')                    
                else:
                    messages.error(request, "Invalid username or password")
                    return redirect('Signin')
            else:
                messages.error(request,"Error while Submitting request please check form and re-submit")
                return redirect('Signin')

@method_decorator(signout_deco, name='get')
class Signout(View):
    def get(self,request):
        logout(request)
        return redirect('Signin')

class password_reset_request(View):
    def get(self,request):
        password_reset_form = PasswordResetForm()
        order_count = Order.objects.filter(user=request.user).count()
        cart_count = Cart.objects.filter(user=request.user).count()    
                        
        context = {"password_reset_form":password_reset_form,'cart_count':cart_count,'order_count':order_count,}
        return render(request, "account/password_reset.html", context) 

    def post(self,request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Yumsuk Journals',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'noreply<support@yumsukjournals.com>' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    except:
                        messages.error(request,'an error occured while trying to send password reset details, Check your internet connection or try again later')
                        return redirect('Signin')
                    return redirect ("/accounts/password_reset/done/")
    
# @login_required(redirect_field_name='next', login_url=None)
# def verify_code(request):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             if not request.user.is_verified:
#                 code = form.cleaned_data.get('code')
#                 if verify.check(request.user.phone, code):
#                     request.user.is_verified = True
#                     request.user.save()
#                     return redirect('home')
#                 else:
#                     messages.error(request, "incorrect verification code")
#                     redirect('verify')
#             else:
#                 redirect('home')
#     else:
#         form = VerifyForm()
#     return render(request, 'core/verify.html', {'form': form})

# @login_required
# def reverify_code(request):
#     phone = request.user.phone
#     verify.send(str(phone))
#     return redirect('verify')

