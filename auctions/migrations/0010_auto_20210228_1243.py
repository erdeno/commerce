# Generated by Django 3.1.7 on 2021-02-28 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210228_0802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='last_bidder',
            new_name='bidder',
        ),
    ]