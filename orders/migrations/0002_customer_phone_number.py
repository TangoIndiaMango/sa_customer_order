# Generated by Django 5.1.5 on 2025-02-01 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(default=2348169739153, max_length=30),
            preserve_default=False,
        ),
    ]
