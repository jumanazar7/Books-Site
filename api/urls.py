from django.urls import path
from .views import GenreListCreateAPIView, GenreRetrieveUpdateDeleteAPIView, BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, AuthorListCreateAPIView, AuthorUpdateDestroyAPIView, PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, ExampleAuthentication


urlpatterns = [
    path('auth/', ExampleAuthentication.as_view()),
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genre/<slug:slug>/', GenreRetrieveUpdateDeleteAPIView.as_view()),
    path('books/', BookListCreateAPIView.as_view()),
    path('book/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view()),
    path('authors/', AuthorListCreateAPIView.as_view()),
    path('author/<int:pk>/', AuthorUpdateDestroyAPIView.as_view()),
    path('posts/', PostListCreateAPIView.as_view()),
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view())
]
