from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

def blog_page(request,slug):
	template = loader.get_template('blog/blog_page.html')
	context = {}
	return HttpResponse(template.render(context, request))
