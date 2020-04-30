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
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = BlogPage.objects.order_by("-id")[0:3]
        events = EventPage.objects.all().live().order_by('date').exclude(date__lt=datetime.now()).order_by('-id')[0:3]
        context['blogpages'] = blogpages
        context['events'] = events
        return context


