from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, FloatBlock
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from django import forms
from .forms import ReviewForm

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from django.contrib.auth.models import User

from wagtail.snippets.models import register_snippet
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Create your models here.


class StoreIndex(Page):
    subpage_types = ['ProductPage']
    


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)



class ProductPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProductPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ProductPage(Page):
    name = models.CharField(max_length=200,blank=True, null=True, help_text="Название товара")
    cost = models.FloatField()
    in_stock = models.IntegerField(default=0)
    sale = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)
    count_rating = models.IntegerField(default=0)
    categories = ParentalManyToManyField('shop.StoreCategory', blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True) 
    option = StreamField([
        ('option', blocks.StructBlock([
            ('name', CharBlock (label="Название параметра")),
            ('cost', FloatBlock(label="Стоимоть товара с параметром", required=False)),

        ], template = 'blocks/shop/option_block.html', icon='openquote', label='Параметры товара')), 
    ], blank=True, null=True)
    short_description = RichTextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('cost'),
            FieldPanel('in_stock'),
            FieldPanel('sale'),
            FieldPanel('short_description'),
            FieldPanel('description'),
        ], heading="Информация по товару"),
        StreamFieldPanel('option', classname="full"),
        InlinePanel('slider', label="Слайдер в превью поста"),
        InlinePanel('related_links', label="Связанные товары"),
        FieldPanel('tags'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
    ]


    parent_page_types = ['shop.StoreIndex']

    def get_context(self, request):
        # Update template context
        context = super().get_context(request)
        form = ReviewForm()
        context['form'] = form
        return context



class ProductGalleryImage(Orderable):
    page = ParentalKey(ProductPage, on_delete=models.CASCADE, related_name='slider')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]


class ProductReview(models.Model):
    product = models.ForeignKey(ProductPage, on_delete=models.SET_NULL, blank=True, null=True)
    author_name = models.CharField(max_length=140)
    author_email = models.EmailField()
    author_url = models.CharField(max_length=200, blank=True, null=True)
    author_avatar = models.URLField(null=True, blank=True)
    review_content = models.CharField(max_length=800,blank=False)
    vote = models.PositiveSmallIntegerField(blank=False)
    pros = models.CharField(max_length=400)
    cons = models.CharField(max_length=400)
    wasrecomeded = models.BooleanField(default=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    publish = models.BooleanField(default=False)


class ProductPageRelatedLink(Orderable):
    shop_product = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)
    page = ParentalKey(ProductPage, on_delete=models.CASCADE, related_name='related_links')
    panels = [
        PageChooserPanel('shop_product', ['shop.ProductPage']),
    ]


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)



class OrderItem(models.Model):
    product = models.ForeignKey(ProductPage, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)



@register_snippet
class StoreCategory(models.Model):
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
        verbose_name_plural = 'Категории (магазин)'



