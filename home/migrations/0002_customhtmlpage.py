# Generated by Django 2.2.13 on 2020-09-02 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomHTMLPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('page_tamplate', models.CharField(blank=True, default='default.html', help_text="Необходимо указывать полное название html файла 'название.html'", max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
