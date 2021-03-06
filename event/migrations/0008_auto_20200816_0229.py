# Generated by Django 2.2.12 on 2020-08-16 02:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_auto_20200510_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='form_answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='max_visitors',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='timepad',
            field=models.URLField(blank=True, help_text='URL на мероприятие в Timepad', null=True),
        ),
    ]
