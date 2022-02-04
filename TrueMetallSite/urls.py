from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predicts/current', views.current_predict, name='current_predict'),
    path('predicts', views.predicts, name='predicts'),
]
