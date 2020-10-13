from django.shortcuts import render

from django.shortcuts import render

#from .forms import UserForm, CommentForm, BlogForm
from .models import User, Product, Purchase, Bag, Rating, Brand, Category, Image, Purchased_Product

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

def pack(_list):
    new_list = zip(_list[::2], _list[1::2])
    return new_list

def get_current_user(req):
    try:
        user_id = req.session["user_id"]
        role = req.session["role"]
        user = User.objects.get(id=user_id)
        return user
    except Exception as error:
        print(error)
        return None  

def get_users_bag(user):
    try:
        bag = Bag.objects.filter(owner=user).first()
        return bag
    except:
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

def get_popular_products(count, product):
    return Product.objects.filter(category=product.category, brand=product.brand).filter(~Q(id = product.id)).order_by('rating')[:count]

def filter_products(request):
    role = session_parameter(request, "role")
    q = get_parameter(request, "q")
    category_id = get_parameter(request, "category")
    category = Category.objects.filter(id=category_id).first()
    optional = get_parameter(request, "optional")
    brand_id = get_parameter(request, "brand")
    brand = Brand.objects.filter(id=brand_id).first()
    blocks = Product.objects.order_by("pub_date")

    if optional == "popular":
        blocks = Product.objects.order_by('ratings__average')
    elif optional == "cheap":
        blocks = Product.objects.order_by("price")
    elif optional == "expencive":
        blocks = Product.objects.order_by("-price")
    else:
        blocks = Product.objects.all()
    if brand:
        blocks = blocks.filter(brand=brand)
    if category:
        blocks = blocks.filter(category=category)
    if q:
        blocks = blocks.filter(Q(name__icontains=q) | Q(price__icontains=q) | Q(description__icontains=q))
                                                                        
    
    blocks = blocks.filter(count_on_shop__gte=0)
    return blocks

def filter_products_with_category(request, category_id):
    role = session_parameter(request, "role")
    q = get_parameter(request, "q")
    
    category = Category.objects.filter(id=category_id).first()
    optional = get_parameter(request, "optional")
    brand_id = get_parameter(request, "brand")
    brand = None
    if brand_id:
        brand = Brand.objects.filter(id=brand_id).first()
    blocks = Product.objects.order_by("pub_date").filter(category__id=category_id)

    if optional == "popular":
        blocks = Product.objects.order_by('ratings__average')
    elif optional == "cheap":
        blocks = Product.objects.order_by("price")
    elif optional == "expencive":
        blocks = Product.objects.order_by("-price")
    else:
        blocks = Product.objects.all()
    if brand:
        blocks = blocks.filter(brand=brand)
    if q:
        blocks = blocks.filter(Q(name__icontains=q) | Q(price__icontains=q) | Q(description__icontains=q))
                                                                        
    
    blocks = blocks.filter(count_on_shop__gte=0)
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
                return render(request, "login.html", {
                    "login_error": "Неправильный логин или пароль!",
                })
        else:
            return render(request, "login.html", {
                "login_error": "Пользователя с таким email не сущетсвует!",
            })

    return render(request, "login.html", {})

def register(request):
    user = True
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            return render(request, "login.html", {
                "register_error": "Пароли не совпадают!",
                "email": email,
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
            return render(request, "login.html", {
                "register_error": "Такой пользователь уже существует!",
                "email": email,
            })
        hash_password = make_pw_hash(password)
        current_user = User.objects.create(email=email, password=hash_password)
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
            request.session["role"] = "user"
            return render(request, "login.html", {
                "notification": "Вам на почту выслано письмо для подтверждения!",
            })
        except Exception as error:
            return render(request, 'message.html', {
                "text" : error,
            })

    return render(request, "login.html", {})

def get_paginated_blogs(request, paginator):
    page = request.GET.get('page')
    try:
        page = int(page)
    except:
        page = 1
    a = ""
    block = ""
    pages=[]
    if page:
        try:
            block = paginator.page(page)
        except EmptyPage:
            block = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        for i in range(page-2, page+3):
            try:
                a = paginator.page(i)
                pages.append(i)
            except:
                continue
        print(pages)
        if pages[-1] != paginator.num_pages:
            pages.append(paginator.num_pages)

        if pages[0] != 1:
            pages.insert(0, 1)
    else:
        pages = [1,2,3,4,5,paginator.num_pages]
        block = paginator.page(1)
    return block, pages

def about(request):
    user = get_current_user(request)
    return render(request, "about.html", {
        "user": user,
    })


def support(request):
    user = get_current_user(request)
    return render(request, "support.html", {
        "user": user,
    })


def contacts(request):
    user = get_current_user(request)
    return render(request, "contacts.html", {
        "user": user,
    })


def product(request, id):
    user = get_current_user(request)
    bag = get_users_bag(user)
    product = Product.objects.filter(id=id).first()
    if not product:
        return redirect(reverse("main:index"))
    return render(request, "product.html", {
        "user": user,
        "bag": bag,
        "product": product,
        "categories": pack(list(Category.objects.all())),
        "popular_products": get_popular_products(6, product),
    })


def products(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    q = get_parameter(request, "q")
    q = "" if not q else q
    brand_id = get_parameter(request, "brand")
    brand = None
    try:
        brand = Brand.objects.get(id=brand_id)
    except:
        pass
    price = get_parameter(request, "price")

    blocks = filter_products(request)

    paginator = Paginator(blocks, COUNT_PRODUCTS_ON_PAGE)
    paginated_blocks, pages = get_paginated_blogs(request, paginator)

    brands = Brand.objects.all()

    return render(request, "products.html", {
        "user": user,
        "bag": bag,
        "pages": pages,
        "products": paginated_blocks,
        "brand": brand,
        "price": price,
        "q": q,
        "price_values": {
            "all": "Цена",
            "cheaper": "Дешевле",
            "expencive": "Дороже"
        },
        "brands": brands,
        "categories": pack(list(Category.objects.all())),
    })

def category(request, id):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()

    q = get_parameter(request, "q")
    q = "" if not q else q
    
    category = Category.objects.filter(id=id).first()

    products = Product.objects.filter(category__id = id)

    brand_id = get_parameter(request, "brand")
    brand = None
    if brand_id != '':
        brand = Brand.objects.filter(id=brand_id).first()

    price = get_parameter(request, "price")

    blocks = filter_products_with_category(request, id)

    paginator = Paginator(blocks, COUNT_PRODUCTS_ON_PAGE)
    paginated_blocks, pages = get_paginated_blogs(request, paginator)

    brands = Brand.objects.all()

    return render(request, "category.html", {
        "user": user,
        "bag": bag,
        "pages": pages,
        "products": paginated_blocks,
        "brand": brand,
        "price": price,
        "q": q,
        "price_values": {
            "all": "Цена",
            "cheaper": "Дешевле",
            "expencive": "Дороже"
        },
        "brands": brands,
        "category": category,
        "categories": pack(list(Category.objects.all())),
    })


def categories(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    return render(request, "categories.html", {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })


def shares(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    return render(request, "shares.html", {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })


def catalog(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    return render(request, "catalog.html", {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })


def cart(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    return render(request, "cart.html", {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })


def thanks(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    return render(request, "thanks.html", {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })

def promotions(request):
    user = get_current_user(request)
    bag = Bag.objects.filter(owner=user).first()
    return render(request, "promotions.html", {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })

def delete_session_parameter(request):
    if request.method == "POST":
        name = post_parameter(request, "name")
        del request.session[name]
    return redirect(reverse("main:myadmin"))

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
        
        return render(request, "index.html", {
            "notification": "Вы успешно подтвердили почту!",
        })
        
    else:
        return render(request, "index.html", {
            "error": "Неверная ссылка активации почты!",
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
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("main:index"))
    if request.method == "POST":
        
        bag = Bag.objects.filter(owner=current_user).first()

        current_path = os.path.abspath(os.path.dirname(__file__))
        images = post_file(request, 'preview')
        description = post_parameter(request, "description")
        name = post_parameter(request, "name")
        category_id = int(post_parameter(request, 'category'))
        brand_id = int(post_parameter(request, 'brand'))
        price = int(post_parameter(request, 'price'))
        count = int(post_parameter(request, 'count'))

        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(id=category_id)
        
        for image in images:
            if not image.name.endswith(".png") and not image.name.endswith(".jpg") and not image.name.endswith(".jpeg"):
                upload_error = "Одна из картинок имеет неверный формат! Допустимые форматы: jpg, png, jpeg" 
                del request.session['admin_success'] 
                request.session['admin_error'] = upload_error
                return redirect(reverse("main:myadmin"))
            
        product = Product.objects.create(name=name, description=description, price=price, count_on_shop=count, category=category, brand=brand)
        count = 1
        for image in images:
            new_img_url = current_path + "\\static\\images\\products\\product" + str(product.id) + "." + str(count) + ".jpg"
            with open(new_img_url, 'wb') as handler:
                for chunk in image.chunks():
                    handler.write(chunk)
            
            static_img_url = "/static/images/products/product" + str(product.id) + "." + str(count) + ".jpg"
            new_image = Image.objects.create(img_url=static_img_url, name=image.name, absolute_path=new_img_url)
            product.images.add(new_image)
            count += 1
        product.save()
        
        request.session['admin_success'] = 'Продукт успешно добавлен!'
        return redirect(reverse('main:myadmin'))
    return redirect(reverse("main:index"))
    
def delete_category(request):
    if request.method == "POST":
        ids = request.POST.getlist("delete_category")
        for id in ids:
            category = Category.objects.filter(id=int(id)).first()
            category.delete_image()
            category.delete()
        request.session['admin_success'] = 'Категория успешно удалена!'
        return redirect(reverse('main:myadmin'))
    else:
        return redirect(reverse('main:index'))

def delete_product(request):
    if request.method == "POST":
        ids = request.POST.getlist("delete_category")
        for id in ids:
            product = Product.objects.filter(id=int(id)).first()
            for image in product.images.all():
                image.delete_image()
                image.delete()
            product.delete()
        request.session['admin_success'] = 'Продукт успешно удален!'
        return redirect(reverse('main:myadmin') + "?delete_category=true")
    else:
        return redirect(reverse('main:index'))

def add_category(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("main:index"))
    if request.method == "POST":
        bag = Bag.objects.filter(owner=current_user).first()

        current_path = os.path.abspath(os.path.dirname(__file__))
        images = post_file(request, 'category_image')
        name = post_parameter(request, "category_name")
        
        for image in images:
            if not image.name.endswith(".png") and not image.name.endswith(".jpg") and not image.name.endswith(".jpeg"):
                upload_error = "Одна из картинок имеет неверный формат! Допустимые форматы: jpg, png, jpeg" 
                del request.session['admin_success'] 
                request.session['admin_error'] = upload_error
                return redirect(reverse("main:myadmin"))
            
        
        category = Category.objects.create(name=name)
        new_img_url = current_path + "\\static\\images\\categories\\category" + str(category.id) + ".jpg"
        with open(new_img_url, 'wb') as handler:
            for chunk in images[0].chunks():
                handler.write(chunk)
        
        static_img_url = "/static/images/categories/category" + str(category.id) + ".jpg"
        category.img_url = static_img_url
        category.absolute_path = new_img_url
        category.save()
        
        request.session['admin_success'] = 'Категория успешно добавлена!'
        return redirect(reverse("main:myadmin"))
    return redirect(reverse("main:index"))

def add_brand(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("main:index"))
    if request.method == "POST":
        bag = Bag.objects.filter(owner=current_user).first()
        name = post_parameter(request, "add_brand")
        
        brand = Brand.objects.create(name=name)
        brand.save()

        request.session['admin_success'] = 'Бренд успешно добавлен!'
        return redirect(reverse("main:myadmin"))
    return redirect(reverse("main:index"))

def delete_brand(request):
    if request.method == "POST":
        ids = request.POST.getlist("delete_brand")
        for id in ids:
            brand = Brand.objects.filter(id=int(id)).first()
            brand.delete()
        
        request.session['admin_success'] = 'Бренд успешно удален!'
        return redirect(reverse('main:myadmin'))
    else:
        return redirect(reverse('main:index'))

def index(request):
    user = get_current_user(request)
    bag = get_users_bag(user)
        
    return render(request, 'index.html', {
        "user": user,
        "bag": bag,
        "preview_categories": Category.objects.all()[:6],
        "categories": pack(list(Category.objects.all())),
    })

def admin_panel(request):
    user = get_current_user(request)
    if not user:
        return redirect(reverse('main:index'))
    if not user.role == "admin":
        return redirect(reverse('main:index'))
    
    products = Product.objects.all()
    bag = get_users_bag(user)

    return render(request, 'admin.html', {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
        "product_categories": Category.objects.all(),
        "brands": Brand.objects.all(),
        "products": products,
    })



def profile(request):
    user = get_current_user(request)
    if not user:
        return redirect(reverse("main:index")) 
    bag = get_users_bag(user)
    return render(request, 'profile.html', {
        "user": user,
        "bag": bag,
        "categories": pack(list(Category.objects.all())),
    })

def add_product_to_bag(request):
    if request.method == "POST":
        
        product_id = post_parameter(request, "product_id")
        if not product_id:
            return JsonResponse({"error": "Нет параметра product_id!"})
        
        product = Product.objects.filter(id=product_id).first()
        
        user = get_current_user(request)
        if not user:
            return JsonResponse({"error": "Not Authorized!"})

        bag = get_users_bag(user)

        for purchased_product in bag.products.all():
            if purchased_product.product == product:
                purchased_product.count += 1
                purchased_product.save()
                return JsonResponse({"success": True})
        new_product = Purchased_Product.objects.create(product=product, count=1)
        bag.products.add(new_product)
        return JsonResponse({"success": True})
    return redirect(reverse("main:index"))

def update_avatar(request):
    if request.method == "POST":
        user = get_current_user(request)
        if not user:
            return redirect(reverse('main:index'))
        image = post_file(request, 'avatar')
        
        try:
            if not image.name.endswith(".png") and not image.name.endswith(".jpg") and not image.name.endswith(".jpeg"):
                upload_error = "Выберите .jpg или .png формат для картинки!" 
                return render(request, 'profile.html', {
                    "user": user,
                    "upload_error": upload_error,
                })
        except:
            upload_error = "Вы не выбрали картинку для аватара!"
            if role == "student": 
                return render(request, 'portfolio_edit.html', {
                    "user": user,
                    "upload_error": upload_error,
                })
            else:
                return render(request, 'employer_profile.html', {
                    "user": user,
                    "upload_error": upload_error,
                })

        new_img_url = '/home/digitalportfolio/Digital-Portfolio/main/static/images/user/avatars/avatar'+str(user.id)+'.jpg'
        with open(new_img_url, 'wb') as handler:
            for chunk in image.chunks():
                handler.write(chunk)
        
        new_img_url = "/static/images/user/avatars/avatar" + str(user.id) + ".jpg"
        user.img_url = new_img_url
        user.save()

    if role == "student":
        return redirect(reverse('main:portfolio_edit'))
    else:
        return redirect(reverse('main:employer_profile'))
    


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