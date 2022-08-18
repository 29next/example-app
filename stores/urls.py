from django.urls import path

from . import views

app_name = 'stores'
urlpatterns = [
    path('auth/login/', views.StoreAuthHandler.as_view(), name='login'),
    path('auth/setup/', views.StoreAuthSetup.as_view(), name='setup'),
    path('<pk>/detail/', views.StoreDetailView.as_view(), name='detail'),
    path('webhooks/', views.StoreWebhookProcessor.as_view(), name='webhook_processor'),
]
