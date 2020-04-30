import os
from datetime import timedelta
from django.db import models
from wagtail.core import blocks
from django.utils import timezone
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel, StreamFieldPanel
from django.shortcuts import render
from django.contrib.auth.models import User

from wagtail.core.blocks import CharBlock, RichTextBlock, RawHTMLBlock, ListBlock, BlockQuoteBlock

from wagtail.snippets.models import register_snippet

from wagtail.search import index

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from ics import Calendar, Event
from ics.alarm import DisplayAlarm
from django.db.models.signals import post_save
from wagtail.core.signals import page_published
from django.dispatch import receiver
from django.core.files.base import ContentFile



class EventIndex(Page):
    subpage_types = ['EventPage']
    calenadar_file = models.FileField(upload_to='uploads/global_ics/', null=True, blank=True)

    def serve(self, request):
        # Get the full unpaginated listing of resource pages as a queryset -
        # replace this with your own query as appropriate
        eventpages = EventPage.objects.child_of(self).live().order_by('date').exclude(date__lt=timezone.now())
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            eventpages = eventpages.filter(tags__name=tag).order_by('date').exclude(date__lt=timezone.now())
        paginator = Paginator(eventpages, 6) # Show 6 resources per page

        page = request.GET.get('page')
        try:
            eventpages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            eventpages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            eventpages = paginator.page(paginator.num_pages)
        return render(request, self.template, {
            'page': self,
            'events': eventpages,
            'eventpages': eventpages,
        })


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'EventPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class EventPage(Page):
    date = models.DateTimeField("Дата мероприятия")
    dateend = models.DateTimeField("Конец мероприятия", blank=True, null=True)
    cost = models.PositiveIntegerField(blank=True, null=True, help_text='Если оставить поле пустым отобразится что мероприятие бесплатное')
    duration = models.DurationField(blank=True, help_text='Если указана дата окончания мероприятия, это поле в приоритете. Формат ввода Дни Часы:Минуты:Секунды')
    ics = models.FileField(upload_to='uploads/', null=True, blank=True)
    intro = RichTextField(blank=False)
    body = StreamField([
        ('emphasize', blocks.CharBlock(label="Выделить текст", icon="title", template = 'blocks/event_emphasize_block.html')),
        ('paragraph', blocks.RichTextBlock(label="Текст", icon="pilcrow", template = 'blocks/event_paragraph_block.html')),
        ('image', ImageChooserBlock(label="Картинка слева", icon="image", template = 'blocks/image_left_block.html')),
        ('image', ImageChooserBlock(label="Картинка справа", icon="image", template = 'blocks/image_right_block.html')),
        ('html', RawHTMLBlock(label="Чистый HTML", icon="code")),
        ('list', blocks.ListBlock(blocks.CharBlock(label="Пункт списка"), icon="list-ul", template = 'blocks/list_block.html')),
        ('blockquote', blocks.StructBlock([
            ('quote', BlockQuoteBlock (label="Цитата")),
            ('author', CharBlock (label="Автор")),
        ], template = 'blocks/quote_block.html', icon='openquote')), 
    ])
    max_visitors = models.PositiveIntegerField(blank=True)
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)
    location = models.CharField(max_length=250, blank=True)
    timepad = models.URLField(
        help_text='URL на мероприятие в Timepad', blank=True)
    categories = ParentalManyToManyField('event.EventCategory', blank=True)
    organizer = models.ForeignKey('event.EventOrganizer', on_delete=models.SET_NULL, null=True, blank=True)
    views = models.IntegerField(default=0)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),

    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('dateend'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Дополнительная информация по новости"),
        FieldPanel('cost'),
        FieldPanel('intro'),
        FieldPanel('duration'),
        FieldPanel('max_visitors'),
        FieldPanel('location'),
        FieldPanel('timepad'),
        StreamFieldPanel('body', classname="full"),
        ImageChooserPanel('main_image'),
        FieldPanel('organizer'),
        InlinePanel('related_links', label="Связанные события"),
    ]

    parent_page_types = ['event.EventIndex']


    def calculate_enddate(self):
        return self.date + self.duration


#work on signal publish page
def create_ics(sender, instance, **kwargs):
    c = Calendar()
    alarm = [DisplayAlarm(trigger=timedelta(minutes=30))]

    e = Event()
    e.name = instance.title
    e.begin = instance.date
    e.end = instance.dateend
    e.alarms = alarm
    if instance.duration != None:
        e.duration = instance.duration
    if (instance.cost == 0 or instance.cost == None):
        cost = 'Бесплатно'
        e.description = str(instance.intro) + ' Стоимость: ' + str(cost)
    else:
        e.description = str(instance.intro) + ' Стоимость: ' + str(instance.cost)+  'р.'
    e.location = instance.location
    if instance.timepad != None:
        e.url = instance.timepad
    c.events.add(e)

    instance.ics.delete(save=False)
    instance.ics.save(instance.title +'.ics', ContentFile(str(c)), save=True)
    #Формирование глобального файла со всеми мероприятиями
    global_ics = EventIndex.objects.all()[0]
    events = global_ics.get_children()
    c = Calendar()
    for event in events:
        e = Event()
        e.name = event.title
        e.begin = event.specific.date
        e.end = event.specific.dateend
        e.alarms = alarm
        if event.specific.duration != None:
            e.duration = event.specific.duration
        if (event.specific.cost == 0 or event.specific.cost == None):
            cost = 'Бесплатно'
            e.description = str(event.specific.intro.strip("<p>*</p>")) + ' Стоимость: ' + str(cost)
        else:
            e.description = str(event.specific.intro.strip("<p>*</p>")) + ' Стоимость: ' + str(event.specific.cost)+  'р.'
        e.location = event.specific.location
        if event.specific.timepad != None:
            e.url = event.specific.timepad
        c.events.add(e)
    global_ics.calenadar_file.delete(save=False)
    global_ics.calenadar_file.save('global.ics', ContentFile(str(c)), save=True)


page_published.connect(create_ics, sender=EventPage, dispatch_uid="my_unique_identifier")




class EventPageRelatedLink(Orderable):
    event_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)
    page = ParentalKey(EventPage, on_delete=models.CASCADE, related_name='related_links')
    panels = [
        PageChooserPanel('event_page', ['event.EventPage']),
    ]


@register_snippet
class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории (мепроприятия)'


@register_snippet
class EventOrganizer(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=40, blank=True)
    website = models.URLField(help_text="Ссылка на сайт организатора", blank=True)
    phone = models.CharField(max_length=19, blank=True)
    address = models.CharField(max_length=50, blank=True)
    avatar = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )


    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('website'),
        FieldPanel('phone'),
        FieldPanel('address'),
        ImageChooserPanel('avatar'),
    ]

    def __str__(self):
        return self.name + ' ' + self.website

    class Meta:
        verbose_name_plural = 'Организаторы мероприятий'