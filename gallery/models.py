from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images import get_image_model

from django.shortcuts import render, redirect
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from taggit.models import Tag
# Create your models here.

class GalleryIndex(RoutablePageMixin,Page):
    intro_title = models.CharField(
        verbose_name=_('Заголовок блока галереии'),
        blank=True,
        max_length=200,
        help_text=_('Необязательный заголовок H1 на с ранице галерии.')
    )
    intro_text = RichTextField(
        blank=True,
        verbose_name=_('Вводный текст'),
        help_text=_('Необязательное введение после заголовка.')
    )
    collection = models.ForeignKey(
        'wagtailcore.Collection',
        verbose_name=_('Collection'),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Показывать изображения в галерее из этой коллекции.')
    )
    images_per_page = models.IntegerField(
        default=8,
        verbose_name=_('Картинок на страницу'),
        help_text=_('Как много картинок отображать на странице.')
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_title', classname='full title'),
        FieldPanel('intro_text', classname='full title'),
        FieldPanel('collection'),
        FieldPanel('images_per_page', classname='full title'),
    ]


    @property
    def images(self, tags=None):
        return get_gallery_images(self.collection.name, self)

    @property
    def tags(self):
        return self.get_gallery_tags()

    def get_context(self, request):
        images = self.images
        tags = self.tags
        context = super(GalleryIndex, self).get_context(request)
        page = request.GET.get('page')
        paginator = Paginator(images, self.images_per_page)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        context['gallery_images'] = images
        context['gallery_tags'] = tags
        return context


    def get_gallery_tags(self, tags=[]):
        images = get_gallery_images(self.collection.name, self, tags=tags)
        for img in images:
            tags += img.tags.all()
        tags = sorted(set(tags))
        return tags


    @route('^tags/ajax/$', name='tag_archive')
    @route('^tags/ajax/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            return redirect(self.url)
        try:
            taglist.append(tag)
        except NameError:
            taglist = []
            taglist.append(tag)

        images = get_gallery_images(self.collection.name, self, tags=taglist)
        tags = self.get_gallery_tags(tags=taglist)
        paginator = Paginator(images, self.images_per_page)
        page = request.GET.get('page')
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        context = self.get_context(request)
        context['gallery_images'] = images
        context['gallery_tags'] = tags
        context['current_tag'] = tag
        return render(request, 'gallery/gallery_ajax.html', context)

def get_gallery_images(collection, page=None, tags=None):
    # Tags must be a list of tag names like ["Hasthag", "Kawabonga", "Winter is coming"]
    images = None
    try:
        images = get_image_model().objects.filter(collection__name=collection).prefetch_related("tags").order_by('id')
    except Exception as e:
        pass
    if images and tags:
        images = images.filter(tags__name__in=tags).prefetch_related("tags").distinct().order_by('id')
    return images