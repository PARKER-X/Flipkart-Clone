# Generated by Django 4.0.2 on 2022-06-10 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]