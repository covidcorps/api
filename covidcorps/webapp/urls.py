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
    path('corpsmembers/<int:pk>/emails', views.ListCorpsMemberEmails.as_view(), name='corpsmembers-emails-list'),
    path('locations/', views.ListLocations.as_view(), name='locations-list'),
    # path('locations/<int:pk>')
    path('locations/<int:pk>/contacts', views.ListLocationContacts.as_view(), name='location-contacts-list'),
    path('locations/<int:pk>/contacts/<int:contact_pk>/phones', views.ListLocationContactPhones.as_view(), name='location-contact-phones-list'),
    path('locations/<int:pk>/contacts/<int:contact_pk>/emails', views.ListLocationContactEmails.as_view(), name='location-contact-emails-list'),

    path('deployments/', views.ListDeployments.as_view(), name='deployments-list'),
    path('locations/<int:location>/deployments', views.ListLocationDeployments.as_view(), name='location-deployments-list'),
    path('corpsmembers/<int:corpsmember>/assignments', views.ListCorpsMemberAssignments.as_view(), name='corpsmember-assignments-list'),
    path('deployments/<int:deployment>/assignments', views.ListDeploymentAssignments.as_view(), name='deployment-assignments-list'),
    path('assignments/', views.ListAssignments.as_view(), name='assignments-list'),



]

urlpatterns = format_suffix_patterns(urlpatterns)