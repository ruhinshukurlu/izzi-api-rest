# Generated by Django 3.2 on 2022-08-08 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220808_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskerskill',
            name='priceType',
            field=models.CharField(blank=True, choices=[('hourlyPrice', 'Hourly Service'), ('fixedPrice', 'Fixed Price')], max_length=50, verbose_name='Price Type'),
        ),
    ]