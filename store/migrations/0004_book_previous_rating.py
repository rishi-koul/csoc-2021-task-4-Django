# Generated by Django 2.2.1 on 2021-07-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210720_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='previous_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
