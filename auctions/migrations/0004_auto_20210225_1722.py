# Generated by Django 3.1.7 on 2021-02-25 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210225_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='category_name',
        ),
    ]
