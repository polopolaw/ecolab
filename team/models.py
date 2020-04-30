from django.contrib.auth.models import User
from django.forms import widgets
from django import forms
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core import blocks
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaForm


class FormField(AbstractFormField):
    page = ParentalKey('JoinForm', on_delete=models.CASCADE, related_name='form_fields')



class JoinForm(WagtailCaptchaForm):
    paragraph = RichTextField(blank=True)
    describe_list = StreamField([
        ('list', blocks.ListBlock(blocks.CharBlock(label="Пункт списка"), icon="list-ul", template = 'blocks/list_block.html')),
    ])

    content_panels = AbstractForm.content_panels + [
        FieldPanel('paragraph', classname="full"),
        StreamFieldPanel('describe_list', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        for name, field in form.fields.items():
            field.label = ''
            # here we want to adjust the widgets on each field
            # if the field is a TextArea - adjust the rows
            #from https://stackoverflow.com/questions/48321770/how-to-modify-attributes-of-the-wagtail-form-input-fields
            if isinstance(field.widget, widgets.Input):
                field.widget.attrs.update({'placeholder': field.help_text})
            if isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({'placeholder': field.help_text, 'rows': 4})
            field.help_text= ''
        return form


@register_snippet
class TeamMemberRole(models.Model):
    name = models.CharField(max_length=40, blank=False, null=True)
    plural = models.CharField(max_length=40, blank=False, null=True, help_text='Название во множественном числе')
    panels = [
        FieldPanel('name'),
        FieldPanel('plural'),
    ]

    class Meta:
        verbose_name_plural = 'Роль в команде проекта'


    def __str__(self):
        return self.name


@register_snippet
class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_userprofile', null=False, blank=False)
    info = models.CharField(max_length=100, blank=True)
    role = models.ForeignKey(TeamMemberRole, models.SET_NULL, null=True, blank=True)
    specificrole = models.CharField(max_length=100, blank=True)
    facebook = models.URLField(
        help_text='Your Facebook page URL',blank=True)
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @', blank=True)
    twitter = models.URLField(
        help_text='URL на аккаунт в Twitter', blank=True)
    vk = models.URLField(
        help_text='URL vk.com', blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('user'),
        FieldPanel('info'),
        FieldPanel('role'),
        FieldPanel('specificrole'),
        ImageChooserPanel('photo'),
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('twitter'),
            FieldPanel('vk'),
        ],heading='Аккаунты в социальных сетях'),
        
    ]

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = 'Команда проекта'

    search_fields = [
        index.SearchField('user'),
        index.SearchField('info'),
    ]




class TeamIndex(Page):
    content_panels = Page.content_panels


    def get_context(self,request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        roles = TeamMemberRole.objects.all().order_by('id')
        context['roles'] = roles
        return context