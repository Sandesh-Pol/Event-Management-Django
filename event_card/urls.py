from django.urls import path
from . import views


urlpatterns = [
    path('cardview/', views.index_view, name='index_view'),
    path('like/<int:event_id>/', views.like_event, name='like_event'),
]
