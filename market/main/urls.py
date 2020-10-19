from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),  
    path('logout', views.logout, name='logout'),  
    path('register', views.register, name='register'),  
    path('about', views.about, name='about'),
    path('support', views.support, name='support'),
    path('product/<int:id>', views.product, name='product'),
    path('search', views.products, name='products'),
    path('contacts', views.contacts, name='contacts'),
    path('categories', views.categories, name='categories'),
    path('shares', views.shares, name='shares'),
    path('catalog', views.catalog, name='catalog'),
    path('cart', views.cart, name='cart'),
    path('thanks', views.thanks, name='thanks'),
    path('profile', views.profile, name='profile'),
    path('add_product', views.add_product, name='add_product'),
    path('delete_product', views.delete_product, name='delete_product'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category', views.delete_category, name='delete_category'),
    path('add_brand', views.add_brand, name='add_brand'),
    path('delete_brand', views.delete_brand, name='delete_brand'),
    path('add_share', views.add_share, name='add_share'),
    path('delete_share', views.delete_share, name='delete_share'),
    path('profile', views.profile, name='profile'),
    path('myadmin', views.admin_panel, name='myadmin'),
    path('delete_session_parameter', views.delete_session_parameter, name='delete_session_parameter'),
    path('add_rating', views.add_rating, name='add_comment'),
    path('add_discount', views.add_discount, name='add_discount'),
    path('delete_discount', views.delete_discount, name='delete_discount'),
    path('add_product_to_bag', views.add_product_to_bag, name='add_product_to_bag'),
    path('delete_product_from_bag', views.delete_product_from_bag, name='delete_product_from_bag'),
    path('delete_one_product_from_bag', views.delete_one_product_from_bag, name='delete_one_product_from_bag'),

    path('download/(?P<path>.*)$', views.download, name="download"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),    
    
]
#