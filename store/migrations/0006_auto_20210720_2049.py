# Generated by Django 2.2.1 on 2021-07-20 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0005_auto_20210720_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0.0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Book')),
                ('specific_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='specific_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='PrevRating',
        ),
    ]
