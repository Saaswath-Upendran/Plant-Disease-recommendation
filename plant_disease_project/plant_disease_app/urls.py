from django.urls import path
from .views import *

app_name = "plant_disease_app"


urlpatterns = [
    path("",home,name="home"),
    path("upload",PredictionView,name="upload")
]