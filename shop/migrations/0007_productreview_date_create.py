# Generated by Django 2.2.12 on 2020-05-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200511_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]