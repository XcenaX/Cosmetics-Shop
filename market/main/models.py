from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    email = models.TextField(default='')
    password = models.TextField(default='')
    fullname= models.TextField(default="") 
    username = models.TextField(default="") 
    balance = models.IntegerField(default=0)
    role = models.TextField(default='user')
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.username


class Comment(models.Model):
    text = models.TextField(default='')
    pub_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Category(models.Model):
    name = models.TextField(default='')
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.TextField(default='')
    price = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    comments = models.ManyToManyField(Comment, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)

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
    count = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.product

class Purchase(models.Model):
    purchased_products = models.ManyToManyField(Purchased_Product, blank=True)
    purhcase_start_date = models.DateTimeField(default=timezone.now)
    purhcase_end_date = models.DateTimeField(blank=True)
    is_delivered = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.owner

class Bag(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.owner

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])