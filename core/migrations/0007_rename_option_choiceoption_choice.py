# Generated by Django 3.2 on 2022-08-09 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_taskerskill_pricetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choiceoption',
            old_name='option',
            new_name='choice',
        ),
    ]
