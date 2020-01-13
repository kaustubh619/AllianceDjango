from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, Http404
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from twilio.rest import Client
import os
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from .serializers import TourPackageSerializer, PackagesSerializer, TourPackageWithPackages, TripCommentSerializer, \
    CategorySerializer, PackageQuerySerializer, PackageQueryCheckedSerializer, BlogSerializer, PackageQuerySerializerWD
from .models import TourPackages, Packages, TripComments, Category, PackageQuery, Blog
from rest_framework import filters


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_admin(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user and user.is_superuser != True:
        return Response({'error': 'Invalid admin credentials'}, status=HTTP_400_BAD_REQUEST)
    elif not user:
        return Response({'error': 'User does not exist'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'id': user.id, 'username': user.username},
                    status=HTTP_200_OK)


@permission_classes((AllowAny,))
class CategoryView(generics.ListAPIView):
    queryset = TourPackages.objects.all()
    serializer_class = TourPackageSerializer


class CategoryPostView(viewsets.ViewSet):
    def category_list(self, request):
        queryset = TourPackages.objects.all()
        serializer = TourPackageSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TourPackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryEditDelete(APIView):
    def get_object(self, pk):
        try:
            return TourPackages.objects.get(id=pk)
        except TourPackages.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = TourPackageSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = TourPackageSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny,))
class PackageView(generics.ListAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer


class PackagePostView(viewsets.ViewSet):
    def package_list(self, request):
        queryset = Packages.objects.all()
        serializer = PackagesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PackagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageEditDelete(APIView):
    def get_object(self, pk):
        try:
            return Packages.objects.get(id=pk)
        except Packages.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = PackagesSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = PackagesSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def handle__uploaded_file(f):
    if not os.path.isdir("media/uppy_images/"):
        os.makedirs("media/uppy_images/")

    with open('media/uppy_images/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    return f.name


@permission_classes((AllowAny,))
class PackageImage(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        print(self.request.FILES)

    def post(self, request, format=None):
        res = {}

        for i in self.request.FILES:
            array = {}
            array['success'] = 1
            res['url'] = 'http://35.154.220.96/media/uppy_images/' + handle__uploaded_file(self.request.FILES[i])
            array['file'] = res
        return Response(array)


@permission_classes((AllowAny,))
class CategoryWithProducts(generics.ListAPIView):
    queryset = TourPackages.objects.all()
    serializer_class = TourPackageWithPackages


@permission_classes((AllowAny,))
class PackageWithIdView(APIView):
    def get_object(self, pk):
        try:
            return Packages.objects.get(id=pk)
        except Packages.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = PackagesSerializer(obj, context={"request": request})
        return Response(Obj.data)


@permission_classes((AllowAny,))
class TripCommentsView(generics.ListAPIView):
    queryset = TripComments.objects.all()
    serializer_class = TripCommentSerializer


@permission_classes((AllowAny,))
class MainCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes((AllowAny,))
class TourPackageWithPackagesView(APIView):
    def get_object(self, pk):
        try:
            return TourPackages.objects.get(id=pk)
        except TourPackages.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = TourPackageWithPackages(obj, context={"request": request})
        return Response(Obj.data)


@permission_classes((AllowAny,))
class PackagesByCategoryId(APIView):
    def get_object(self, pk):
        try:
            return Packages.objects.filter(category=pk)
        except Packages.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = PackagesSerializer(obj, context={"request": request}, many=True)
        return Response(Obj.data)


@permission_classes((AllowAny,))
class GetCategoryById(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Packages.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CategorySerializer(obj, context={"request": request})
        return Response(Obj.data)


@permission_classes((AllowAny,))
class PackageQueryPostView(viewsets.ViewSet):
    def package_query_list(self, request):
        queryset = PackageQuery.objects.all()
        serializer = PackageQuerySerializerWD(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PackageQuerySerializerWD(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class PackageQueryPostViewWithDepth(viewsets.ViewSet):
    def package_query_list_wd(self, request):
        queryset = PackageQuery.objects.all()
        serializer = PackageQuerySerializer(queryset, many=True)
        return Response(serializer.data)


class PackageQueryById(APIView):
    def get_object(self, pk):
        try:
            return PackageQuery.objects.get(id=pk)
        except PackageQuery.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = PackageQuerySerializer(obj, context={"request": request})
        return Response(Obj.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PackageQueryCheckedById(APIView):
    def get_object(self, pk):
        try:
            return PackageQuery.objects.get(id=pk)
        except PackageQuery.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = PackageQueryCheckedSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = PackageQueryCheckedSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class UncheckedQuery(generics.ListAPIView):
    queryset = PackageQuery.objects.filter(read=False)
    serializer_class = PackageQuerySerializer


class MainCategoryDeleteEdit(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = CategorySerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MainCategoryPostView(viewsets.ViewSet):
    def theme_list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class PackageSearch(generics.ListCreateAPIView):
    search_fields = ['name', 'package_city_routes']
    filter_backends = (filters.SearchFilter,)
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer


@permission_classes((AllowAny,))
class BlogView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogPostView(viewsets.ViewSet):
    def blog_list(self, request):
        queryset = Blog.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDeleteEdit(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = BlogSerializer(obj, context={"request": request})
        return Response(Obj.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = BlogSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny,))
class BlogByIdForHome(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        Obj = BlogSerializer(obj, context={"request": request})
        return Response(Obj.data)


@permission_classes((AllowAny,))
class BlogSearch(generics.ListCreateAPIView):
    search_fields = ['title', 'content']
    filter_backends = (filters.SearchFilter,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer






