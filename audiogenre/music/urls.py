from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommendations/<int:emotion_index>/', views.recommendations, name='recommendations'),
    path('select_mood/', views.select_mood, name='select_mood'),
]
