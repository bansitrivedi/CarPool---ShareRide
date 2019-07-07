from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.template import RequestContext
# Create your views here.

def home(request): 
    return render(request, 'home/home.html')


def about(request):
        return render(request, 'home/about.html')

def faq(request):
        return render(request, 'home/faq.html')

def handler404(request, exception, template_name="404.html"):
    data = {}
    return render(request,'home/404.html', data)

def handler500(request):
    data = {}
    return render(request,'home/500.html', data)
