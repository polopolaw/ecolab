# Generated by Django 2.2.12 on 2020-08-16 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_productreview_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='publish',
            field=models.BooleanField(default=False),
        ),
    ]
