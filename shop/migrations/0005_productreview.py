# Generated by Django 2.2.12 on 2020-05-11 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200511_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=80)),
                ('author_surname', models.CharField(max_length=90)),
                ('author_email', models.EmailField(max_length=254)),
                ('author_url', models.CharField(blank=True, max_length=200, null=True)),
                ('author_avatar', models.URLField(blank=True, null=True)),
                ('review_content', models.CharField(max_length=800)),
                ('vote', models.PositiveSmallIntegerField()),
                ('pros', models.CharField(max_length=400)),
                ('cons', models.CharField(max_length=400)),
                ('wasrecomeded', models.BooleanField(blank=True, default=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.ProductPage')),
            ],
        ),
    ]
