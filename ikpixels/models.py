from django.db import models
from django.contrib.auth.models import User
from music_nation.models import Customer
from ckeditor.fields import RichTextField
from  embed_video.fields  import  EmbedVideoField
from cloudinary.models import CloudinaryField


CATEGORY = (
	('Event','Event-Tickets Marketing'),
	('Music','Music Upload'),
	('Music_Purchase','Buying Music'),
	)

PAYMENT_METHOD= (
	('TNM','TNM Mpamba'),
	('Airtel','Airtel Money'),
	('NB','National Bank')
	)

#MUC(Music Upload code uplode),MDC(Music download code),EUC(Event upload code),
class PymtCode(models.Model):
	codeOwner = models.CharField(max_length=100,null=True,blank=True)# property rights
	codeOwnerNumber = models.CharField(max_length=100,null=True,blank=True)
	Mid = models.CharField(max_length=100,null=True,blank=True)# for item id
	customer = models.CharField(max_length=100)
	codeValue =  models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
	code = models.CharField(max_length=100,null=True,blank=True)
	paid = models.BooleanField(default= False) #if owner received money
	active = models.BooleanField(default=True)

	def __str__(self):
		return  self.Mid + '-' + self.code 

class MusicorEventPayment(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	payment_method = models.CharField(max_length=40,choices=PAYMENT_METHOD)
	item_id = models.CharField(max_length=100,default="0")
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
	category = models.CharField(max_length=40,choices=CATEGORY)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	PaymentReferenceNumber =models.CharField(max_length=100)
	aprove = models.BooleanField(default=False)

	def __str__(self):
		return self.category


class IKspotify(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	spotify_id = models.URLField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.spotify_id

