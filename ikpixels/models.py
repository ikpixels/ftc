from django.db import models
from django.contrib.auth.models import User
from music_nation.models import Customer
from ckeditor.fields import RichTextField
from  embed_video.fields  import  EmbedVideoField
from cloudinary.models import CloudinaryField


CATEGORY = (
	('Event','Event Tickets'),
	('Music','Music Upload'),
	)

PAYMENT_METHOD= (
	('TNM','TNM Mpamba'),
	('Airtel','Aitel Money'),
	('NB','National Bank')
	)

#MUC(Music Upload code uplode),MDC(Music download code),
class PymtCode(models.Model):
	Mid = models.CharField(max_length=100,null=True,blank=True)# for music id
	customer = models.CharField(max_length=100)
	code = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.code

class MusicorEventPayment(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	payment_method = models.CharField(max_length=40,choices=PAYMENT_METHOD)
	amount = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
	category = models.CharField(max_length=40,choices=CATEGORY)
	created_at = models.DateTimeField(auto_now_add=True)
	PaymentReferenceNumber =models.CharField(max_length=100)
	aprove = models.BooleanField(default=False)

	def __str__(self):
		return self.category