# Generated by Django 2.2.12 on 2020-05-11 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productreview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='author_surname',
        ),
        migrations.AlterField(
            model_name='productreview',
            name='author_name',
            field=models.CharField(max_length=140),
        ),
    ]
