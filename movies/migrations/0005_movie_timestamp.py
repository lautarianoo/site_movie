# Generated by Django 3.1.7 on 2021-04-06 08:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20210405_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
