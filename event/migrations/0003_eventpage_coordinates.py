# Generated by Django 2.2.12 on 2020-05-01 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200430_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='coordinates',
            field=models.CharField(blank=True, help_text='Широта,долгота через пробел', max_length=100, null=True),
        ),
    ]
