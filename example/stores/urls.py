from django.urls import path

from . import views

urlpatterns = [
    path('setup/', views.setup, name='setup'),
    path('authcode/', views.auth_code, name='authcode'),
]
