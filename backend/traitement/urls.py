from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.TraitementCreateView.as_view(),name='traitement-create'),
    path('list/',views.TraitementListView.as_view(),name='traitement-list') ,
    path('detail/<int:pk>/',views.TraitementDetailView.as_view(),name='traitement-detail') ,
    path('update/<int:pk>/',views.TraitementUpdateView.as_view(),name='traitement-update') ,
    path('delete/<int:pk>/',views.TraitementDeleteView.as_view(),name='traitement-delete') ,
]