from django.db import models
from wagtail.core import blocks
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
# Create your models here.

@register_setting
class WorkspaceSettings(BaseSetting):
    address = models.CharField(max_length=255, help_text='Адрес пространства, указывается на сайте', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=17)
    working_hours = StreamField([
        ('working_days', blocks.CharBlock(label="День")),
        ('working_hours', blocks.CharBlock(label="Время")),
    ])

    panels = [
        FieldPanel('address'),
        FieldPanel('email'),
        FieldPanel('phone'),
        StreamFieldPanel('working_hours', classname="full"),
    ]

    class Meta:
        verbose_name = "Контакты, время работы"



@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL',blank=True)
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @', blank=True)
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL', blank=True)
    twitter = models.URLField(
        help_text='URL на аккаунт в Twitter', blank=True)
    vk = models.URLField(
        help_text='URL vk.com', blank=True)


    panels = [
    MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
            FieldPanel('twitter'),
            FieldPanel('vk'),
        ],heading='Аккаунты в социальных сетях')
    ]

    class Meta:
    	verbose_name = "Аккаунты в социальных сетях"



@register_setting
class SubscribeFormSettings(BaseSetting):
    subscribe_form_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    panels = [
        # note the page type declared within the pagechooserpanel
        PageChooserPanel('subscribe_form_page', ['subscribe.SubscribePage']),
    ]

    class Meta:
        verbose_name = "Форма подписки email"