from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from blog.models import Article


def root(request):
    return HttpResponseRedirect('/home')

def home_page(request):
    articles = Article.objects.filter(draft = False).order_by('-published_date').all()
    context = {'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def article_details(request, id):
    article = Article.objects.get(pk=id)
    context = {'article': article}
    response = render(request, 'article.html', context)
    return HttpResponse(response)
