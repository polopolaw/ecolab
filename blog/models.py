from django.db import models
from datetime import datetime, timedelta
from django import forms
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet



from event.models import EventPage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from subscribe.models import SubscribePage

class BlogIndex(Page):
    # Speficies that only BlogPage objects can live under this index page
    subpage_types = ['BlogPage']

     # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        news_pages = BlogPage.objects.live().descendant_of(self)
        for page in news_pages:
            # Not tags.append() because we don't want a list of lists
            tags += page.tags.all()
        tags = sorted(set(tags))
        return tags

    def children(self):
        return self.get_children().specific().live()

    def serve(self, request):
        # Get the full unpaginated listing of resource pages as a queryset -
        # replace this with your own query as appropriate
        blogpages = BlogPage.objects.child_of(self).live().order_by('-date')
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogpages = blogpages.filter(tags__name=tag)
        category = request.GET.get('cat')
        if category:
            blogpages = blogpages.filter(categories__name=category)
        paginator = Paginator(blogpages, 6) # Show 6 resources per page

        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogpages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogpages = paginator.page(paginator.num_pages)
        events = EventPage.objects.all().live().order_by('date').exclude(date__lt=datetime.now()).order_by('-id')[0:3]
        popularnews = BlogPage.objects.filter(date__gte = datetime.now() - timedelta(days=60)).live().filter().order_by(('-views'))[:3]
        categories = BlogCategory.objects.all()
        return render(request, self.template, {
            'page': self,
            'posts': blogpages,
            'blogpages': blogpages,
            'events': events,
            'popularnews': popularnews,
            'categories': categories,
            'site_url': request.build_absolute_uri(),
        })

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
   
    # Database fields
    main_embed = models.TextField(blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField()
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    views = models.IntegerField(default=0)

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]


    # Editor panels configuration

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Дополнительная информация по новости"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('main_image'),
        FieldPanel('main_embed'),
        InlinePanel('slider', label="Слайдер в превью поста"),
        InlinePanel('related_links', label="Связанные новости"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]


    # Parent page / subpage type rules

    parent_page_types = ['blog.BlogIndex']
    subpage_types = []

    def counter(self):
        self.views +=1
        self.save()


    def get_popular_news(self):
        popularnews = BlogPage.objects.filter(date__gte = datetime.now() - timedelta(days=60)).live().filter().order_by(('-views'))[:3]
        return popularnews

    def get_context(self, request):
        # Update template context
        context = super().get_context(request)
        categories = BlogCategory.objects.all()
        events = EventPage.objects.all().live().order_by('date').exclude(date__lt=datetime.now()).order_by('-id')[0:3]
        popularnews = BlogPage.objects.filter(date__gte = datetime.now() - timedelta(days=60)).live().filter().order_by(('-views'))[:3]
        context['popularnews'] = popularnews
        context['events'] = events
        context['categories'] = categories
        context['site_url'] = request.build_absolute_uri()
        return context

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='slider')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class BlogPageRelatedLink(Orderable):
    blog_post = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='related_links')
    panels = [
        PageChooserPanel('blog_post', ['blog.BlogPage']),
    ]


@register_snippet
class BlogCategory(models.Model):
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
        verbose_name_plural = 'Категории (блог)'