# Generated by Django 2.2.13 on 2020-09-10 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_slidertohomepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slidertohomepage',
            name='button_text_2',
            field=models.CharField(blank=True, max_length=90, null=True),
        ),
    ]