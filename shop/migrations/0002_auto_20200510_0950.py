# Generated by Django 2.2.12 on 2020-05-10 09:50

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpage',
            name='option',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Название параметра')), ('cost', wagtail.core.blocks.FloatBlock(label='Стоимоть товара с параметром', required=False))], blank=True, icon='openquote', label='Параметры товара', null=True, template='blocks/shop/quote_block.html'))]),
        ),
        migrations.CreateModel(
            name='StoreCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name_plural': 'Категории (магазин)',
            },
        ),
        migrations.CreateModel(
            name='ProductPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='shop.ProductPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_productpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='productpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='shop.StoreCategory'),
        ),
        migrations.AddField(
            model_name='productpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='shop.ProductPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
