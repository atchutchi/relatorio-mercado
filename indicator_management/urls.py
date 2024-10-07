from django.urls import path
from . import views

urlpatterns = [
    path('indicators/', views.IndicatorListView.as_view(), name='indicator_list'),
    path('indicators/update/<int:pk>/', views.IndicatorUpdateView.as_view(), name='indicator_update'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('indicators/create/', views.IndicatorCreateView.as_view(), name='indicator_create'),
    path('indicators/import/', views.IndicatorImportView.as_view(), name='indicator_import'),  # Nova rota adicionada
    path('indicators/export/', views.IndicatorExportView.as_view(), name='indicator_export'),  # Nova rota adicionada
    path('indicators/delete/<int:pk>/', views.IndicatorDeleteView.as_view(), name='indicator_delete'),
]