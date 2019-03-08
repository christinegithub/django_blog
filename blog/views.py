from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from blog.models import Article, Topic, Comment, CommentForm, ArticleForm


def root(request):
    return HttpResponseRedirect('/home')

def home_page(request):
    articles = Article.objects.filter(draft = False).order_by('-published_date').all()
    context = {'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def article_details(request, id):
    article = Article.objects.get(pk=id)
    context = {'article': article, 'form': CommentForm()}
    response = render(request, 'article.html', context)
    return HttpResponse(response)

def new_article(request):
    context = {'form': ArticleForm()}
    response = render(request, 'new_article.html', context)
    return HttpResponse(response)

def create_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save()
        return HttpResponseRedirect('/home')
    else:
        print(form.errors)

def create_article(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        new_article = form.save()
        return HttpResponseRedirect('/home')
    else:
        print(form.errors)
