from django.contrib import admin
from django.urls import path
from ikpixels import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = "ikpixels"

urlpatterns = [
    path('ticket/',views.ticket,name='ticket'),
    path('music/',views.music,name='music'),
    path('payment/<user>/',views.paymentDetail,name='paymentDetail'),
    path('pricing/',views.pricing,name='pricing'),
    path('upload_payment/',views.upload_payments,name='upload_payment'),
    path('Payment/<item>/<int:id>/',views.upload_payments,name='purchese_payment'),
    path('uprove_upload_pymt/',views.uprove_upload_pymt,name='uprove_upload_pymt'),
    path('moneyTocken/',views.userMoney,name='money'),
    path('payment/success/', LoginView.as_view(template_name='ik/payment_success.html'), name="payment_success"),
    ]