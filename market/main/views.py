from django.shortcuts import render

from django.shortcuts import render

#from .forms import UserForm, CommentForm, BlogForm
from .models import User, Product, Purchase, Bag, Rating

from django.shortcuts import redirect
from django.urls import reverse

from .modules.hashutils import check_pw_hash, make_pw_hash

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone

import smtplib, ssl

from .modules.sendEmail import send_email

from django.http import HttpResponse
from django.http import JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

import os
from django.conf import settings
from django.http import HttpResponse, Http404

from django.db.models import Q

from django.views.generic import DetailView, TemplateView

COUNT_PRODUCTS_ON_PAGE=20

def get_current_user(req):
    try:
        user = None
        user_id = req.session["user_id"]
        role = req.session["role"]
        user = User.objects.get(id=user_id)
    except Exception as error:
        return None  

def get_parameter(request, name):
    try:
        return request.GET[name]
    except:
        return None 

def post_parameter(request, name):
    try:
        return request.POST[name]
    except:
        return None 

def post_file(request, name):
    try:
        return request.FILES.getlist(name)
    except:
        return None

def session_parameter(request, name):
    try:
        return request.session[name]
    except:
        return None

def filter_products(request):
    role = session_parameter(request, "role")
    q = get_parameter(request, "q")
    category = get_parameter(request, "category")
       
    if category == "new":
        blocks = Product.objects.order_by("pub_date")
    elif category == "popular":
        blocks = Product.objects.filter(ratings__isnull=False).order_by('ratings__average')
    elif category == "cheap":
        blocks = Product.objects.order_by("price")
    elif category == "expencive":
        blocks = Product.objects.order_by("-price")
    else:
        blocks = Product.objects.all()
    if q:
        blocks = blocks.filter(Q(content__icontains=q) | Q(title__icontains=q) | Q(salary__icontains=q))
                                                                        
    
    blocks = blocks.filter(is_available=True)
    return blocks

def logout(request):
    if request.method == "POST":
        try:
            del request.session["user_id"]
            del request.session["role"]
        except:
            print("error")
    return redirect(reverse('main:login'))

def login(request):
    user = None
    if request.method == "POST":
        email = post_parameter(request, "email")
        password = post_parameter(request, "password")
        
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        
        if user:
            if check_pw_hash(password, user.password):
                request.session["user_id"] = user.id
                request.session["role"] = user.role
                return redirect(reverse('main:index'))
            else:
                return redirect(reverse('main:index'), kwargs={
                    "notification": "Неправильный логин или пароль!",
                    "notification_type": "login_error"
                })
        else:
            return redirect(reverse('main:index'), kwargs={
                "notification": "Пользователя с таким email не сущетсвует!",
                "notification_type": "login_error"
            })
    return redirect(reverse('main:index'))

def register(request):
    user = True
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            return redirect(reverse('main:index'), kwargs={
                "notification": "Пароли не совпадают!",
                "notification_type": "register_error",
                "email": email,
                "username": username,
            })

        if len(password) < 5:
            return redirect(reverse('main:index'), kwargs={
                "notification": "Пароль должен быть не менее 5 символов!",
                "notification_type": "register_error",
                "email": email,
                "username": username,
            })

        try:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                raise Exception
            users = User.objects.filter(email=email)
            if len(users) > 0:
                raise Exception
        except:
           user = False
        
        if not user:
            return redirect(reverse('main:index'), kwargs={
                "notification": "Такой пользователь уже существует!",
                "notification_type": "register_error",
                "email": email,
                "username": username,
            })
        hash_password = make_pw_hash(password)
        current_user = User.objects.create(email=email, password=hash_password, username=username)
        current_user.save()
        bag = Bag.objects.create(owner=current_user)
        bag.save()
        

        try:
            current_site = get_current_site(request)
            mail_subject = 'Активируйте свой аккаунт!'
            message = render_to_string('active_email.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token':account_activation_token.make_token(current_user),
                "mail_subject": mail_subject,
            })
            to_email = current_user.email
            
            send_email(message, mail_subject, to_email)
            request.session["user_id"] = current_user.id
            request.session["role"] = role
            return redirect(reverse('main:index'), kwargs={
                "notification": "Вам на почту выслано письмо для подтверждения!",
                "notification_type": "notification",
            })
        except Exception as error:
            return render(request, 'message.html', {
                "text" : error,
            })

    return render(request, "register.html", {})


def about(request):
    return render(request, "about.html", {})


def contacts(request):
    return render(request, "contacts.html", {})


def categories(request):
    return render(request, "categories.html", {})


def catalog(request):
    return render(request, "catalog.html", {})


def activate(request, uidb64, token):
    user = None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Exception):
        user = None

    if not user:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Exception):
            user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return redirect(reverse('main:index'), kwargs={
            "notification": "Вы успешно подтвердили почту!",
            "notification_type": "notification",
        })
        
    else:
        return redirect(reverse('main:index'), kwargs={
            "notification": "Неверная ссылка активации почты!",
            "notification_type": "error"
        })

def rate_product(request):
    if request.method == "POST":
        product_id = post_parameter("id")
        stars = post_parameter("stars")
        product = Product.objects.filter(pk=product_id).first()
        user = get_current_user()
        rating = Rating.objects.create(product, int(stars), user)
        rating.save()
        return render(request, 'product.html', {
            "product": product,
            "user": user,
        })

    return redirect(reverse("main:index")) 

def add_product(request):
    if request.method == "POST":
        product_images = post_file(request, 'files')
        # дописать добавление продукта

def index(request):
    q = get_parameter(request, "q")
    q = "" if not q else q
    category = get_parameter(request, "category")
    user = get_current_user(request)
    blocks = filter_products(request)
        
    return render(request, 'index.html', {
        "user": user,
        "blocks": blocks,
        "q": q,
        "category": category,
    })

    


def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404