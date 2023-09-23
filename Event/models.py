from django.db import models
from django.db import models
from django.contrib.auth.models import User
from music_nation.models import Customer
from ckeditor.fields import RichTextField
from  embed_video.fields  import  EmbedVideoField
from Store.models import Product

from cloudinary.models import CloudinaryField
# Create your models here.


DISTRICT = (('Balaka','Balaka'),
            ('Blantyre','Blantyre'),
            ('Chikwawa','Chikwawa'),
            ('Chiradzuru','Chiradzuru'),
            ('Chitipa','Chitipa'),
            ('Dedza','Dedza'),
            ('Dowa','Dowa'),
            ('Karonga','Karonga'),
            ('Kasungu','Kasungu'),
            ('Likoma','Likoma'),
            ('Lilongwe','Lilongwe'),
            ('Machinga','Machinga'),
            ('Mangochi','Mangochi'),
            ('Mchinji','Mchinji'),
            ('Mulanje','Mulanje'),
            ('Mwanza','Mwanza'),
            ('Mzimba','Mzimba'),
            ('Neno','Neno'),
            ('Nkhata_Bay','Nkhata_Bay'),
            ('Nkhotakota','Nkhotakota'),
            ('Nsanje','Nsanje'),
            ('Ntcheu','Ntcheu'),
            ('Ntchisi','Ntchisi'),
            ('Phalombe','Phalombe'),
            ('Ruphi','Ruphi'),
            ('Salima','Salima'),
            ('Thyolo','Thyolo'),
            ('Zomba','Zomba'),
            ('Others','Others')
            )


CATEGORY = (
       ('Conferences','Conferences'),
       ('Music shows','Music shows'),
       ('Sports','Sports'),
       ('Trade shows','Trade shows'),
       ('Seminars','Seminars'),
       ('Company meetings and off-sites','Company meetings and off-sites'),
       ('Team building','Team building'),
       ('Product or service launch','Product or service launch'),
       ('Weddings','Weddings'),
       ('Festivals','Festivals'),
       ('Exhibitions','Exhibitions'),
       ('Charity events','Charity events'),
       ('Fashion shows and red carpets','Fashion shows and red carpets'),
    )


class ticketsCategory(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class ticketsManager(models.Manager):
    def get_queryset(self):
        tickets = super(ticketsManager, self).get_queryset().filter(ticket=True)
        return tickets

class ObjectManager(models.Manager):
    def get_queryset(self):
        tickets = super(ObjectManager, self).get_queryset().filter(ticket=False)
        return tickets

class Ticket(models.Model):

    client = models.ForeignKey(User,on_delete=models.CASCADE)
    ticket = models.BooleanField(default=False)
    ticketCategory = models.CharField(max_length=100,choices=CATEGORY,default="Music shows")
    name = models.CharField(max_length=40)
    simple_discription = models.CharField(max_length=40)

    number_of_tickets = models.PositiveIntegerField(default=0)
    ticket_booked = models.PositiveIntegerField(default=0)
    district = models.CharField(max_length=40,choices=DISTRICT,default="Mwanza")
    venue = models.CharField(max_length=40,null=True,blank=True)
    from_t  = models.TimeField(null=True,blank=True) 
    from_d  = models.DateField(max_length=40,null=True,blank=True)

    to_t  = models.TimeField(null=True,blank=True) 
    to_d  = models.DateField(max_length=40,null=True,blank=True)

    regular_price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
    vip_price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)#for tickets

    description = RichTextField(null=True,blank=True)
    youtube_video_link = EmbedVideoField(null=True,blank=True)

    product_image=  models.ImageField(upload_to='Events/%y/%m/%d',null=True,blank=True)


    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    ticketObjects  = ticketsManager()
    Object = ObjectManager()
  
    def __str__(self):
        return self.name



APPROVED =(
	('Approved','Paid'),
	('Pending','Pending')
	)

class tickets_order(models.Model):
	user   = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,null=True,related_name="order")
	paid   = models.CharField(max_length=40,choices=APPROVED,default="Pending")
	ticket_number = models.CharField(max_length=100,null=True,blank=True)
	ticket_type = models.CharField(max_length=100,null=True,blank=True)
	amount = models.CharField(max_length=100,null=True,blank=True)
	ref = models.CharField(max_length=100,null=True,blank=True)
	payment_mathod = models.CharField(max_length=100,null=True,blank=True)
	account_num =  models.CharField(max_length=100,null=True,blank=True)

	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)

    