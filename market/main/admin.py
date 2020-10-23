from django.contrib import admin
from .models import User, Bag, Product, Purchase, Purchased_Product, Category, Rating, Brand, Image, Share, Purchased_Share

admin.site.register(User)
admin.site.register(Bag)
admin.site.register(Purchase)
admin.site.register(Purchased_Product)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Brand)
admin.site.register(Image)
admin.site.register(Share)
admin.site.register(Purchased_Share)