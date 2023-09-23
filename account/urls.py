from django.contrib import admin
from django.urls import path
from account import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = "account"

urlpatterns = [
    path('truck_ticket_order/',views.truck_ticket_order,name='truck_ticket_order'),
    path('profile/',views.profile,name="profile"),
    # signUp new user /signup/
    path('signup/',views.signup, name='signup'),
    # login the user /login/
    path('login/',views.login_view,name='login'),
    #path('login/', LoginView.as_view(template_name='account/signin.html'), name="login"),
    #logout the current user
    path('logout/', LogoutView.as_view(), name='logout'),
    path('adminAproveMusic/',views.adminAproveMusic, name='adminAproveMusic'),
    ]