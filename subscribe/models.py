from django.db import models
from django.forms import widgets

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.admin.mail import send_mail



# Create your models here.
class FormField(AbstractFormField):
	page = ParentalKey(
		'SubscribePage',
		on_delete=models.CASCADE,
		related_name='form_fields',
	) 

class SubscribePage(AbstractEmailForm):

	template = "subscribe/subscribe_page.html"
	intro = RichTextField(blank=True)
	thank_you_text = RichTextField(blank=True)

	content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"),
    ]

	def send_mail(self, form):
		# `self` is the FormPage, `form` is the form's POST data on submit

		# Email addresses are parsed from the FormPage's addresses field
		addresses = [x.strip() for x in self.to_address.split(',')]
		subject = self.subject
		content = self.thank_you_text
		send_mail(subject, content, addresses, self.from_address)

	def get_form(self, *args, **kwargs):
		form = super(AbstractEmailForm, self).get_form(*args, **kwargs)

		for name, field in form.fields.items():
			field.label = ''
			# here we want to adjust the widgets on each field
			# if the field is a TextArea - adjust the rows
			#from https://stackoverflow.com/questions/48321770/how-to-modify-attributes-of-the-wagtail-form-input-fields
			if isinstance(field.widget, widgets.Input):
				field.widget.attrs.update({'placeholder': field.help_text})
			field.help_text= ''
		return form

