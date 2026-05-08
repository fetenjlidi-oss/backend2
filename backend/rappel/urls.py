from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.RappelCreateView.as_view(),name='rappel-create'),
    path('list/',views.RappelListView.as_view(),name='rappel-list') ,
    path('detail/<int:pk>/',views.RappelDetailView.as_view(),name='rappel-detail') ,
    path('update/<int:pk>/',views.RappelUpdateView.as_view(),name='rappel-update') ,
    path('delete/<int:pk>/',views.RappelDeleteView.as_view(),name='rappel-delete') ,
    path('snooze/<int:pk>/',views.RappelSnoozeView.as_view(),name='rappel-snooze') ,
    path('confirm/<int:pk>/',views.RappelConfirmView.as_view(),name='rappel-confirm') ,
    path('cancel-snooze/<int:pk>/',views.RappelCancelSnoozeView.as_view(),name='rappel-cancel-snooze') ,
    path('snoozed-count/',views.GetNumbreOfRappelsIsSnoozedView.as_view(),name='rappel-snoozed-count') ,
]