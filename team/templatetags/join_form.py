from django import template
from team.models import JoinForm

register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_join_form(context):
    request = context['request']
    join_form = JoinForm.objects.all().first().specific
    form = join_form.get_form()
    return {'form': join_form, 'q':form}