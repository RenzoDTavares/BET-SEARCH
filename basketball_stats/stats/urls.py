from django.urls import path
from . import views

urlpatterns = [
    # A URL principal que chama a função 'index' da view
    path('', views.index, name='index'),
]
