from django.urls import path
from . import views

urlpatterns = [
    path('cardview', views.index_view, name='index_view'),
    path('increment_likes/<int:event_id>/', views.increment_likes, name='increment_likes'),
]
