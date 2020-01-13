from django.contrib import admin
from .models import TourPackages, Packages, TripComments, Category, PackageQuery, Blog

admin.site.register(TourPackages)
admin.site.register(Packages)
admin.site.register(TripComments)
admin.site.register(Category)
admin.site.register(PackageQuery)
admin.site.register(Blog)
