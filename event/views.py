from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from .models import EventPage
# Create your views here.


def ajax_event_index_page(request):
    responseData = {
        'id': 4,
        'name': 'Test Response',
        'roles' : ['Admin','User']
    }

    return JsonResponse(responseData)


@csrf_protect
def register_on_event(request):
    if request.method == 'POST':
        event = EventPage.objects.get(pk=request.POST.get('event_id'))
        result = {event.form_answers.__len__() + 1:{},
        }
        for streamblocks in event.body:
            if(streamblocks.block_type == 'form'):
                for field in request.POST:
                    for blocks in streamblocks.value:
                        if(blocks.id == field):
                            if(blocks.block_type == 'checkbox'):
                                result[event.form_answers.__len__() + 1][blocks.value.get('name')] = request.POST.getlist(field)
                            result[event.form_answers.__len__() + 1][blocks.value.get('name')] = request.POST.get(field, '')
        event.form_answers.update(result)
        event.save()
        messages.add_message(request, messages.SUCCESS, 'Вы успешно зарегистрировались на мероприятие.')
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
                    'request': request,
                }
                html_content = render_to_string(
                    template_name='event/email/ticket_after_registration.html', context=context
                ).strip()
                msg = EmailMultiAlternatives(subject, 'from@example.com', text_content, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.content_subtype = "html"
                msg.send()
                
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context = {
                    'event':event,
                    'user':user,
                    'request': request,
                }
            return render(request, template_name='event/email/ticket_after_registration.html', context=context)
    else:
        return HttpResponseRedirect(request.META.get('/'))