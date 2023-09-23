# Generated by Django 4.2.4 on 2023-09-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikpixels', '0002_musicoreventpayment_name_musicoreventpayment_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pymtcode',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pymtcode',
            name='codeOwner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pymtcode',
            name='codeOwnerNumber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pymtcode',
            name='codeValue',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='pymtcode',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]