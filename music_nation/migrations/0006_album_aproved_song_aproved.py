# Generated by Django 4.2.4 on 2023-09-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_nation', '0005_customer_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='aproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='song',
            name='aproved',
            field=models.BooleanField(default=False),
        ),
    ]
