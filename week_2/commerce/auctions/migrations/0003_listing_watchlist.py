# Generated by Django 4.2.6 on 2023-11-01 03:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]