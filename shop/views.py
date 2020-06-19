from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import ProductReview, ProductPage
from .forms import ReviewForm

from django.contrib import messages



def add_review(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            product = ProductPage.objects.get(pk=request.POST['product'])
            review = ProductReview()
            review.product = product
            review.author_name = form.cleaned_data['author_name']
            review.author_email = form.cleaned_data['author_email']
            review.author_url = form.cleaned_data['author_url']
            review.author_avatar = form.cleaned_data['author_avatar']
            review.review_content = form.cleaned_data['review_content']
            review.vote = form.cleaned_data['vote']
            review.pros = form.cleaned_data['pros']
            review.cons = form.cleaned_data['cons']
            review.wasrecomeded = form.cleaned_data['wasrecomeded']
            messages.add_message(request, messages.SUCCESS, 'Спасибо за ваш отзыв, вскоре он появится после модерации администрацией')
            product.rating = product.rating + form.cleaned_data['vote']
            product.count_rating = product.count_rating + 1
            review.save()
            product.save()
            # redirect to a new URL:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # if a GET (or any other method) we'll create a blank form
    else:
        HttpResponseRedirect('/')

    return HttpResponseRedirect('/')