# Generated by Django 2.2.12 on 2020-08-22 09:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20200816_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='form_answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]