from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from blog.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


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

@login_required
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
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.user = request.user
            new_article = form.save()
            return HttpResponseRedirect('/home')
    else:
        form = ArticleForm()
        context = {'form': form}
        response = render(request, 'new_article.html', context)
        return HttpResponse(response)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
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

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    response = render(request, 'signup.html', context)
    return HttpResponse(response)

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, pk = id, user = request.user.pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.user = request.user
            article.pk = article.id
            edit_article = form.save()
            return HttpResponseRedirect('/articles/'+str(article.pk))
    else:
        form = ArticleForm()

    context = {'article': article, 'form': form}
    response = render(request, 'edit_article.html', context)
    return HttpResponse(response)
