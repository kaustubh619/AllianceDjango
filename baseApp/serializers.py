from rest_framework import serializers
from .models import TourPackages, Packages, TripComments, Category, PackageQuery, Blog


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TourPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TourPackages
        fields = '__all__'


class PackagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Packages
        fields = '__all__'


class TourPackageWithPackages(serializers.ModelSerializer):
    packages = PackagesSerializer(many=True, read_only=True)

    class Meta:
        model = TourPackages
        fields = ['id', 'name', 'info', 'packages']


class TripCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripComments
        fields = '__all__'


class PackageQuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageQuery
        fields = '__all__'

        depth = 1


class PackageQueryCheckedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageQuery
        fields = ['read']


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'


class PackageQuerySerializerWD(serializers.ModelSerializer):

    class Meta:
        model = PackageQuery
        fields = '__all__'


