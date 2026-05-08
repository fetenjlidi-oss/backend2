from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.PatientCreateView.as_view(), name='patient-create'),
    path('list/', views.PatientListView.as_view(), name='patient-list'),
    path('detail/<int:id>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('update/<int:id>/', views.PatientUpdateView.as_view(), name='patient-update'),
    path('delete/<int:id>/', views.PatientDeleteView.as_view(), name='patient-delete'),
    path('search/', views.PatientSearchView.as_view(), name='patient-search'),
    path("patients/login/", views.PatientLoginView.as_view(), name="patient-login"),
    path("patient/count/", views.PatientCountView.as_view(), name="patient-count"),
    path('patients/<int:patient_id>/statistics/', views.PatientStatisticsView.as_view(), name='patient-statistics'),

]