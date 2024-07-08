from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse
from django.views.generic import ListView,TemplateView
from .models import Post
from .tasks import log_message_task,generatelog,testfolder_task,rungeneration
from django.core.files import File
import time
# Create your views here.
#def home_page_view(request):
#    return HttpResponse("Hello, World!")

def trigger_log_task(request):
    log_message_task.delay()  # Call the task asynchronously
    return render(request, 'generate.html')

def trigger_generate(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text:
            return HttpResponseBadRequest("Text input cannot be empty")
        task = rungeneration.delay(text)
        while not task.ready():
            time.sleep(1)  # Sleep for a while before polling again
        if task.successful():
            image_path = task.result
            if image_path:
                createitem(image_path, text)
        else:
            generatelog("Task failed to generate image")
    return render(request, 'generate.html')

def trigger_test_folder(request):
    testfolder_task.delay()  
    return render(request, 'generate.html')

def createitem(image, txt):
    try:
        #Post.objects.create(img=img,text=txt)
        post = Post(text=txt)
        post.img.name = image
        post.save()
    except Exception as e:
        generatelog(e)
    
    
    
class HomePageView(ListView):
    model = Post
    template_name = "home.html"



class AboutPageView(TemplateView):  
    template_name = "about.html"    

class GeneratePageView(TemplateView):  
    template_name = "generate.html"    