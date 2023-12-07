from django.urls import path
from . import views

urlpatterns = [
    path('', views.name, name='name'),
    path('reviews', views.show_reviews, name='show_reviews'),

]
