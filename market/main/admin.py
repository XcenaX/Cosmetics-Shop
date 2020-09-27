from django.contrib import admin
from .models import User, Bag, Product, Purchase, Purchased_Product, Category, Comment

admin.site.register(User)
admin.site.register(Bag)
admin.site.register(Purchase)
admin.site.register(Purchased_Product)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)