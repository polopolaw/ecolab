# Generated by Django 2.2.17 on 2020-11-22 04:14

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200816_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpage',
            name='option',
            field=wagtail.core.fields.StreamField([('option', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Название параметра')), ('cost', wagtail.core.blocks.FloatBlock(label='Стоимоть товара с параметром', required=False)), ('in_stock', wagtail.core.blocks.BooleanBlock(label='Наличие товара с опцией', required=False))], icon='openquote', label='Параметры товара', template='blocks/shop/option_block.html'))], blank=True, null=True),
        ),
    ]
