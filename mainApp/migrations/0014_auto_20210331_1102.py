# Generated by Django 3.1.7 on 2021-03-31 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_auto_20210331_1033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='q',
            new_name='stock',
        ),
    ]
