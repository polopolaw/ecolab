# Generated by Django 2.2.12 on 2020-05-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_eventpage_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='coordinates',
            field=models.CharField(blank=True, help_text='Широта,долгота через запятую', max_length=100, null=True),
        ),
    ]
