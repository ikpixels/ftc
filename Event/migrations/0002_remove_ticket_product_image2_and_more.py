# Generated by Django 4.2.4 on 2023-09-21 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='product_image2',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='Events/%y/%m/%d'),
        ),
    ]
