from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import CompetitionRegister


from django.contrib import messages



def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        r = CompetitionRegister()
        r.name = request.POST['name']
        r.email = request.POST['email']
        r.soc_url= request.POST.getlist('category', "not set")
        r.category = request.POST['category']
        messages.add_message(request, messages.SUCCESS, 'Вы успешно зарегистрироваты, посетите нашу группу вконтакте за подробной информацией.')
        r.save()
        # redirect to a new URL:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # if a GET (or any other method) we'll create a blank form
