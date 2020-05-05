from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import EventPage
# Create your views here.


def ajax_event_index_page(request):
    print('sdfsdfs')
    responseData = {
        'id': 4,
        'name': 'Test Response',
        'roles' : ['Admin','User']
    }

    return JsonResponse(responseData)


@csrf_protect
def register_on_event(request):
    if request.method == 'POST':
        event = get_object_or_404(EventPage, pk=request.POST.get('event_id'))
        result = {event.form_answers.__len__() + 1:{},
        }
        for streamblocks in event.body:
            if(streamblocks.block_type == 'form'):
                for field in request.POST:
                    for blocks in streamblocks.value:
                        if(blocks.id == field):
                            if(blocks.block_type == 'checkbox'):
                                result[blocks.value.get('name')] = request.POST.getlist(field)
                            result[event.form_answers.__len__() + 1][blocks.value.get('name')] = request.POST.get(field, '')
        event.form_answers.update(result)
        event.save()
        try:
            user = result[event.form_answers.__len__()]['Имя']
        except KeyError:
            user = ''
        try:
            to = result[event.form_answers.__len__()]['Email']
        except KeyError:
            to = False
        if to:
            try:
                subject = 'Билет на мероприятие' + event.title
                text_content = 'This is an important message.'
                context = {
                    'event':event,
                    'user':user,
                }
                html_content = render_to_string(
                    template_name='event/email/ticket_after_registration.html', context=context
                ).strip()
                msg = EmailMultiAlternatives(subject, text_content, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.content_subtype = "html"
                msg.send()
                send_mail(subject, html_content, 'from@example.com', [to],  html_message=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/')
        else:
            responseData = {
            'id': 4,
            'name': 'Test Response',
            'roles' : ['Admin','User']
            }
            return JsonResponse(responseData)
    else:
        pass