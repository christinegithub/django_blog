from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def root(request):
    return HttpResponseRedirect('/home')

def home_page(request):
    response = render(request, 'index.html')
    return HttpResponse(response)
