from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('home', views.index_view, name='index_view'),
    path('register', views.register_user, name='register_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('success', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error', views.error_page, name='error'),
    path('verification', views.verification_view, name='verification_view'),
    path('varify', views.put_otp, name='put_otp'),
]
