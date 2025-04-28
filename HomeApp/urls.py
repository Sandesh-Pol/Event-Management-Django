from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_view, name='base_view'),
    path('details/<int:event_id>/', views.details_view, name='details_view'),
    path('like/<int:event_id>/', views.like_event, name='like_event'),
    path('share/<int:event_id>/<str:platform>/', views.share_event, name='share_event'),
    path('profile/', views.profile_view, name='profile_view'),
]
