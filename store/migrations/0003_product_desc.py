# Generated by Django 4.0.2 on 2022-06-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_order_shippingaddress_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
