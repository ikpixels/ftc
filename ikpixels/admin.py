from django.contrib import admin
from . models import PymtCode,MusicorEventPayment

class PymtAdmin(admin.ModelAdmin):
  list_display = ('user', 'payment_method','amount','PaymentReferenceNumber')
  list_per_page=12
  search_fields=['paymentCode']

admin.site.register(MusicorEventPayment,PymtAdmin)
admin.site.register(PymtCode)
