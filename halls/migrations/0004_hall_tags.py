# Generated by Django 3.0.8 on 2020-09-12 23:47

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0003_hall_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='hall',
            name='tags',
            field=django_mysql.models.ListCharField(models.CharField(max_length=20), blank=True, max_length=105, size=5),
        ),
    ]