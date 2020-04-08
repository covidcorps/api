from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, models, serializers

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.ListAccounts.as_view(), name='account-list'),
    path('accounts/<int:pk>', views.DetailAccounts.as_view(), name='account-detail'),
    path('accounts/<int:pk>/<str:action>', views.DetailAccountUpdate.as_view(), name='account-detail-update'),

    path('corpsmembers/', views.ListCorpsMembers.as_view(), name='corpsmembers-list'),
    # path('corpsmembers/<int:pk>', views.DetailResource.as_view(resource=models.CorpsMember, serializer=serializers.CorpsMemberSerializer), name='corpsmember-detail'),
    path('corpsmembers/<int:pk>', views.CorpsMemberDetailHydrated.as_view(), name='corpsmember-detail'),
    path('corpsmembers/<int:pk>/hydrate', views.CorpsMemberDetailHydrated.as_view(), name='corpsmember-detail-hydrated'),
    path('corpsmembers/<int:pk>/phones', views.ListCorpsMemberPhones.as_view(), name='corpsmembers-phones-list'),
    path('corpsmembers/<int:cm_pk>/phones/<int:pk>', views.DetailResource.as_view(resource=models.CorpsMemberPhoneNumber, serializer=serializers.CorpsMemberPhoneSerializer), name='corpsmembers-phone-detail'),
    path('corpsmembers/<int:pk>/emails', views.ListCorpsMemberEmails.as_view(), name='corpsmembers-emails-list'),
    path('corpsmembers/<int:cm_pk>/emails/<int:pk>', views.DetailResource.as_view(resource=models.CorpsMemberEmail, serializer=serializers.CorpsMemberEmailSerializer), name='corpsmembers-email-detail'),
    path('locations/', views.ListLocations.as_view(), name='locations-list'),
    path('locations/<int:pk>', views.DetailResource.as_view(resource=models.Location, serializer=serializers.LocationSerializer), name='location-detail'),
    # path('locations/<int:pk>/contacts', views.ListLocationContacts.as_view(), name='location-contacts-list'),
    path('locations/<int:pk>/contacts', views.ManyResource.as_view(), name='location-contacts-list'),
    path('locations/<int:loc_pk>/contacts/<int:pk>', views.DetailResource.as_view(resource=models.LocationContact, serializer=serializers.LocationContactsSerializer), name='location-contact-detail'),
    path('locations/<int:pk>/contacts/<int:contact_pk>/phones', views.ListLocationContactPhones.as_view(), name='location-contact-phones-list'),
    path('locations/<int:loc_pk>/contacts/<int:contact_pk>/phones/<int:pk>', views.DetailResource.as_view(resource=models.LocationContactPhoneNumber, serializer=serializers.LocationContactPhoneSerializer), name='location-contact-phone-detail'),
    path('locations/<int:pk>/contacts/<int:contact_pk>/emails', views.ListLocationContactEmails.as_view(), name='location-contact-emails-list'),
    path('locations/<int:loc_pk>/contacts/<int:contact_pk>/emails/<int:pk>', views.DetailResource.as_view(resource=models.LocationContactEmail, serializer=serializers.LocationContactEmailSerializer), name='location-contact-email-detail'),

    path('deployments/', views.ListDeployments.as_view(), name='deployments-list'),
    path('deployments/<int:pk>', views.DetailResource.as_view(resource=models.Deployment, serializer=serializers.DeploymentSerializer), name='deployment-detail'),
    path('locations/<int:location>/deployments', views.ListLocationDeployments.as_view(), name='location-deployments-list'),
    path('locations/<int:location_pk>/deployments/<int:pk>', views.DetailResource.as_view(resource=models.Deployment, serializer=serializers.DeploymentSerializer), name='locations-deployment-detail'),
    # path('corpsmembers/<int:corpsmember>/assignments', views.ListCorpsMemberAssignments.as_view(), name='corpsmember-assignments-list'),
    path('corpsmembers/<int:corpsmember>/assignments', views.ManyResource.as_view(), name='corpsmember-assignments-list'),
    # path('corpsmembers/<int:corpsmember>/deployments', views.ManyResource.as_view(), name='corpsmember-assignments-list'),
    # path('deployments/<int:deployment>/assignments', views.ListDeploymentAssignments.as_view(), name='deployment-assignments-list'),
    path('assignments/', views.ListAssignments.as_view(), name='assignments-list'),
    path('assignments/<int:pk>', views.DetailResource.as_view(resource=models.Assignment, serializer=serializers.AssignmentSerializer), name='assignment-detail'),
    re_path(r'.+', views.view_router, name='list-resource')
]

urlpatterns = format_suffix_patterns(urlpatterns)