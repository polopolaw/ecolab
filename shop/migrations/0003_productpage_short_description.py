# Generated by Django 2.2.12 on 2020-05-11 00:09

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200510_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpage',
            name='short_description',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]