from django.urls import path
from .views import HomePageView,AboutPageView,GeneratePageView
from .views import trigger_log_task,trigger_generate
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("generate/", GeneratePageView.as_view(), name="generate"),
    path('trigger-task/', trigger_log_task, name='trigger_task_view'),
    path('trigger-generate/', trigger_generate, name='trigger_generate'),
]
