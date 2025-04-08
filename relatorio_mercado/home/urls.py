from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('api/chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chatbot/reset/', views.reset_chatbot, name='reset_chatbot'),
]