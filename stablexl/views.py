from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,TemplateView
from .models import Post
# Create your views here.
#def home_page_view(request):
#    return HttpResponse("Hello, World!")




class HomePageView(ListView):
    model = Post
    template_name = "home.html"

class AboutPageView(TemplateView):  
    template_name = "about.html"    