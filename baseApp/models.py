from django.db import models
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to='category_images', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class TourPackages(models.Model):
    name = models.CharField(max_length=500)
    info = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name)


class Packages(models.Model):
    category = models.ForeignKey(Category, related_name='category_packages', on_delete=models.PROTECT, blank=True, null=True)
    tour_package = models.ForeignKey(TourPackages, related_name='packages', on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=500)
    price = models.IntegerField()
    duration = models.IntegerField()
    package_city_routes = models.CharField(max_length=500)
    itinerary = models.TextField()
    inclusion = models.TextField()
    exclusion = models.TextField()
    policy_and_terms = models.TextField()
    images = models.TextField()

    def __str__(self):
        return str(self.name)


class TripComments(models.Model):
    customer_image = models.ImageField(upload_to='customer_images', null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    customer_location = models.CharField(max_length=200)
    trip_name = models.CharField(max_length=200)
    customer_comment = models.TextField()

    def __str__(self):
        return str(self.customer_name)


class PackageQuery(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.package) + " - " + str(self.name)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    added_date = models.DateField(default=datetime.now, blank=True, null=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='blog_images', blank=True, null=True)

    def __str__(self):
        return str(self.title)