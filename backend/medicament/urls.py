from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.MedicamentCreateView.as_view(),name='medicament-create'),
    path('list/',views.MedicamentListView.as_view(),name='medicament-list') ,
    path('detail/<int:pk>/',views.MedicamentDetailView.as_view(),name='medicament-detail') ,
    path('update/<int:pk>/',views.MedicamentUpdateView.as_view(),name='medicament-update') ,
    path('delete/<int:pk>/',views.MedicamentDeleteView.as_view(),name='medicament-delete') ,
]