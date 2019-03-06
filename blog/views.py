from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from blog.models import Article, Topic, Comment


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

def create_comment(request):
    article = request.POST['article']
    comment_name = request.POST['comment-name']
    comment_message = request.POST['comment-message']
    comment_article = Article.objects.get(id=article)
    comment = Comment.objects.create(article=comment_article, name=comment_name, message=comment_message)
    return HttpResponseRedirect('/articles/'+ article)
