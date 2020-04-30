from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
from django.http import HttpResponseNotFound
# Create your views here.


def ajax_event_index_page(request):
    print('sdfsdfs')
    responseData = {
        'id': 4,
        'name': 'Test Response',
        'roles' : ['Admin','User']
    }

    return JsonResponse(responseData)

