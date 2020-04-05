from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, models, serializers

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.ListAccounts.as_view(), name='account-list'),
    path('accounts/<int:pk>', views.DetailAccounts.as_view(), name='account-detail'),
    path('accounts/<int:pk>/<str:action>', views.DetailAccountUpdate.as_view(), name='account-detail-update'),

    path('corpsmembers/', views.ListCorpsMembers.as_view(), name='corpsmembers-list'),
    path('corpsmembers/<int:pk>/phones', views.ListCorpsMemberPhones.as_view(), name='corpsmembers-phones-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)