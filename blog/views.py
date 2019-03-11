from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from blog.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

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
        messages.error(request, form.errors)
        return render(request, 'article.html', {'form': CommentForm()})

def create_article(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        new_article = form.save()
        return HttpResponseRedirect('/home')
    else:
        messages.error(request, form.errors)
        return render(request, 'new_article.html', {'form':ArticleForm()})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username = username, password = pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')
