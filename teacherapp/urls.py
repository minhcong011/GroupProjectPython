from django.urls import path
from . import views

urlpatterns = [
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
]