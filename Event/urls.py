from django.contrib import admin
from django.urls import path
from Event import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = "Event"

urlpatterns = [
    path('events/',views.events,name='events'),
    path('add_event/',views.add_event,name="event_terms"),
    path('admin_aprove_ticket/',views.admin_aprove_ticket,name='admin_aprove_ticket'),
    path('Event/<int:id>/',views.event_detail,name="event-detail"),
    path('Admin_Event/<int:id>/',views.admin_event_detail,name="admin_event_detail"),
    path('customer_event_booked/',views.customer_event_booked,name="customer_event_booked"),
    path('ticket_order/<int:id>/',views.ticket_order,name="ticket_order"),
    path('approve_order/<int:id>/',views.approve_order,name="approve_order"),
    ]