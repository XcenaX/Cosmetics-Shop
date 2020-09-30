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
    path('contacts', views.contacts, name='contacts'),
    path('categories', views.categories, name='categories'),
    path('add_product', views.add_product, name='add_product'),

    path('download/(?P<path>.*)$', views.download, name="download"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),    
    
]