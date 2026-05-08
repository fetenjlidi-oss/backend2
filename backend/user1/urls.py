from django.urls import path

from .views import (

    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    UserLoginView
)

urlpatterns = [
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/login/", UserLoginView.as_view(), name="user-detail"),

]