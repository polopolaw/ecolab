from django.db import models
from django import forms
from datetime import datetime
from modelcluster.fields import ParentalKey
from wagtail.users.forms import UserEditForm, UserCreationForm
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from blog.models import BlogPage
from event.models import EventPage

class HomePage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('slider', label="Слайдер в шапке"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = BlogPage.objects.order_by("-id")[0:3]
        events = EventPage.objects.all().live().order_by('date').exclude(date__lt=datetime.now()).order_by('-id')[0:3]
        context['blogpages'] = blogpages
        context['events'] = events
        return context


class SliderToHomePage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='slider')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    title = models.CharField(max_length=90, help_text="Заголовок")
    sub_title = models.CharField(max_length=90, help_text="Подзаголовок")
    button_text_1 = models.CharField(max_length=90)
    button_href_1 = models.URLField(blank=True)
    button_text_2 = models.CharField(max_length=90, blank=True, null=True)
    button_href_2 = models.URLField(blank=True)
    
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('sub_title'),
        MultiFieldPanel([
        FieldPanel('button_text_1'),
        FieldPanel('button_href_1'),
        ]),
        MultiFieldPanel([
        FieldPanel('button_text_2'),
        FieldPanel('button_href_2'),
        ]),
        
    ]

class CustomHTMLPage(Page):
    
    page_template = models.CharField(max_length=100, default='default.html', blank=True, help_text="Необходимо указывать полное название html файла 'название.html'")

    content_panels = Page.content_panels + [
        FieldPanel('page_template'),
    ]

    def get_template(self, request):
        return 'custom/'+self.page_template