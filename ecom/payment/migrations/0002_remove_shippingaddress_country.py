# Generated by Django 5.1.5 on 2025-02-05 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='country',
        ),
    ]
