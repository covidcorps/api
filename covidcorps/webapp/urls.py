from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='registration'),
    path('accounts/', views.ListAccounts.as_view(), name='account-list'),
    path('accounts/<int:pk>', views.DetailAccounts.as_view(), name='account-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)