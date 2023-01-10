from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .serializers import GenreSerializer, AuthorSerializer, BookSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from library.models import Genre, Book, Author
from rest_framework import status, generics, mixins
from .models import Post
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsAuthorOrReadOnly, CustomDjangoModelPermissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from .paginations import CustomPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import filters



class GenreListCreateAPIView(generics.GenericAPIView):
    """Bu yerda description bo'ladi"""
    serializer_class = GenreSerializer
    pagination_class = CustomPagination
    queryset = Genre.objects.all()

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class GenreRetrieveUpdateDeleteAPIView(APIView):
    serializer_class = GenreSerializer

    def get(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        serializer = self.serializer_class(genre)
        return Response(data=serializer.data)

    def put(self, request, slug):
        data = request.data
        genre = get_object_or_404(Genre, slug=slug)
        serializer = self.serializer_class(instance=genre, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def patch(self, request, slug):
        data = request.data
        genre = get_object_or_404(Genre, slug=slug)
        serializer = self.serializer_class(instance=genre, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(data={"deleted": "Genre deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookCreateAPIView(generics.CreateAPIView):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()

class BookListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['author', 'genres']
    search_fields = ['title', 'desc']


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

class AuthorUpdateDestroyAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()
    permission_classes = [IsAuthorOrReadOnly,]


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()
    permission_classes = [IsAuthorOrReadOnly]


class ExampleAuthentication(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication, SessionAuthentication]

    def get(self, request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(content)