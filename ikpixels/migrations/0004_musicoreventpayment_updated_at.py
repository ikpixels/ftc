# Generated by Django 4.2.4 on 2023-09-22 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikpixels', '0003_pymtcode_active_pymtcode_codeowner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicoreventpayment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
