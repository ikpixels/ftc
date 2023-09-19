from django.db import models
from django.contrib.auth.models import User
from music_nation.models import Customer
from ckeditor.fields import RichTextField
from  embed_video.fields  import  EmbedVideoField
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
class category(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Product(models.Model):

    client = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=40)
    gallary = models.BooleanField(default=False)
    simple_discription = models.CharField(max_length=40)
    district = models.CharField(max_length=40,choices=DISTRICT,default="Mwanza")
    price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)#for tickets
    description = RichTextField(null=True,blank=True)
    youtube_video_link = EmbedVideoField(null=True,blank=True)
    weblink = models.URLField(null=True,blank=True)
    product_image=  CloudinaryField('product_image',null=True,blank=True)
    product_image2= CloudinaryField('product_image',null=True,blank=True)
    product_image3= CloudinaryField('product_image',null=True,blank=True)
    product_image4= CloudinaryField('product_image',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
PAYMENT_CHOICES = (
        ('TNM','Mpamba'),
        ('Airtel','Aitel Money'),
        ('NB','National Bank'),
    )
class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )

    customer=models.ForeignKey( Customer, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    payment_method = models.CharField(max_length=20,null=True,choices=PAYMENT_CHOICES)
    refu = models.CharField(max_length=20,null=True)
    acc_Name = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    amount = models.CharField(max_length=50,null=True,blank=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)

class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
