from django.urls import path
from . import views

urlpatterns = [
    path('indicators/', views.IndicatorListView.as_view(), name='indicator_list'),
    path('indicators/update/<int:pk>/', views.IndicatorUpdateView.as_view(), name='indicator_update'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
]