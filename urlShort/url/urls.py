from django.urls import path

from . import views

app_name = 'url'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:key>', views.redirect, name='redirect')
]
