# Generated by Django 2.2.3 on 2021-05-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0007_producto_descuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='nuevo',
            field=models.BooleanField(default=False),
        ),
    ]
