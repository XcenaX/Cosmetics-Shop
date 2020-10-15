from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import os

class Image(models.Model):
    img_url = models.TextField(default='')
    name = models.TextField(default='')
    absolute_path = models.TextField(default='')
    
    def delete_image(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        length = len(product.images.all())
        current_path = os.path.abspath(os.path.dirname(__file__))

        for i in range(1, length+1):
            new_img_url = current_path + "\\static\\images\\products\\product" + str(product.id) + "." + str(i) + ".jpg"
            os.remove(new_img_url)

        
        

class User(models.Model):
    email = models.TextField(default='')
    password = models.TextField(default='')
    first_name = models.TextField(default="") 
    last_name = models.TextField(default="") 
    balance = models.IntegerField(default=0)
    role = models.TextField(default='user')
    is_active = models.BooleanField(default=False)
    img_url = models.TextField(default='/static/images/icons/user.png')
    def __str__(self):
        return self.first_name

class Category(models.Model):
    name = models.TextField(default='')
    img_url = models.TextField(default='')
    absolute_path = models.TextField(default='')
    
    def delete_image(self, category_id):
        category = Category.objects.filter(id=category_id).first()
        length = len(category.images.all())
        current_path = os.path.abspath(os.path.dirname(__file__))

        for i in range(1, length+1):
            new_img_url = current_path + "\\static\\images\\categories\\category" + str(category.id) + "." + str(i) + ".jpg"
            os.remove(new_img_url)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.TextField(default='')
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    price = models.IntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    brand =  models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True)
    count_on_shop = models.IntegerField(null=True, blank=True, default=0)
    

    def is_available(self):
        if count_on_shop <= 0:
            return False
        else:
            return True

    def number_of_ratings(self):
        ratings = Rating.objects.filter(product=self)
        return len(ratings)
    
    def avarage_rating(self):
        ratings = Rating.objects.filter(product=self)
        summa = 0
        for rating in ratings:
            summa += rating.stars
        if len(ratings) > 0:
            return summa / len(ratings)
        else:
            return 0

    def __str__(self):
        return self.name



class Purchased_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_total_price(self):
        price = self.product.price
        return price * self.count

    def __str__(self):
        return self.product.name

class Purchase(models.Model):
    purchased_products = models.ManyToManyField(Purchased_Product, blank=True)
    purhcase_start_date = models.DateTimeField(default=timezone.now)
    purhcase_end_date = models.DateTimeField(blank=True)
    is_delivered = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.owner

class Bag(models.Model):
    products = models.ManyToManyField(Purchased_Product, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def count_of_products(self):
        count = 0
        for purchased_product in self.products.all():
            count += purchased_product.count
        return count

    def sum_of_products(self):
        sum = 0
        for purchased_product in self.products.all():
            for i in range(purchased_product.count):
                sum += purchased_product.product.price
        return sum

    def __str__(self):
        return self.owner.first_name

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    text = models.TextField(default='')
    pub_date = models.DateTimeField(default=timezone.now)