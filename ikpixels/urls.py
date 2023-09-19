from django.contrib import admin
from django.urls import path
from ikpixels import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = "ikpixels"

urlpatterns = [
    path('ticket/',views.ticket,name='ticket'),
    path('music/',views.music,name='music'),
    path('upload_payment/',views.upload_payments,name='upload_payment'),
    ]