from django.urls import path
from . import views

urlpatterns = [
    path('cardview/', views.index_view, name='index_view'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('like/<int:event_id>/', views.like_event, name='like_event'),
    path('share_event/<int:event_id>/<str:platform>/', views.share_event, name='share_event'),
]
