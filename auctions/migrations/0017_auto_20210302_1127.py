# Generated by Django 3.1.7 on 2021-03-02 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_listing_last_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='last_bidder',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
