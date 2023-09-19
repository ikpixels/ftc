from django.contrib import admin
from django.urls import path
from Store import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = "store"

urlpatterns = [
    path('store/',views.store,name='store'),
    path('store/<int:id>/',views.product,name='product'),
    path('search', views.search_view,name='search'),

    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),


    path('my-order', views.my_order_view,name='my-order'),
    path('admin_add_product',views.admin_add_product_view,name="admin_add_product"),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),

    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),

]