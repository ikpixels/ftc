from django.contrib import admin
from . models import tickets_order,ticketsCategory,Ticket
# Register your models here.

admin.site.register(tickets_order)
admin.site.register(Ticket)
admin.site.register(ticketsCategory)