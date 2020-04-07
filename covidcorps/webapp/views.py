from typing import ClassVar, List, Optional

from django.db.models import Model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import Template
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.list import (BaseListView,
                                       MultipleObjectTemplateResponseMixin)
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView, get_view_name
from rest_framework.serializers import Serializer

from . import handlers, models, serializers

import io


def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")

# class JSONResponseMixin:
#     """
#     Renders JSON responses
#     """
#     serializer = None # This must be set by the implementing class should be set to a rest_framework.serializer.Serializer class

#     def render_to_json_response(self, context, **response_kwargs):
#         """
#         Returns JSON response
#         """
#         rv = self.get_data(context)
#         print('data')
#         print(rv)
#         return JsonResponse(
#             # self.get_data(context),
#             rv.data,
#             safe=False,
#             **response_kwargs
#         )

#     def get_data(self, context):
#         # Sanity check that concrete class set the serializer value
#         print(type(context))
#         print(context)
#         assert self.serializer is not None

#         inst = context[self.context_object_name]
#         if self.request.method == 'GET':
#             # GET requested, serialize model instance and return
#             return self.serializer(inst, many=isinstance(inst, list))
        
#         # POST requested, get data in context and create an instance from it
#         return self.serializer(data=inst).data


# class HybridListView(JSONResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
#     """
#     Base class for my list views. Allows both HTML and JSON responses to routes
#     """

#     def render_to_response(self, context, **response_kwargs):
#         # We look for the route to be suffixed with '.json'
#         if self.request.path.endswith('.json'):
#             # A JSON response has been requested
#             return self.render_to_json_response(context, **response_kwargs)
#         return super().render_to_response(context, **response_kwargs)


# class AccountList(HybridListView):
#     """
#     Views for the list routes for the account resource
#     """
#     model = Account
#     context_object_name = 'accounts'
#     serializer = serializers.AccountSerializer



class ListResourceMixin:
    def _parse_and_deserialize(self, request: HttpRequest, **kwargs) -> Serializer:
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
        if kwargs:
            data.update(kwargs)
        return self.serializer(data=data)


class ListAccounts(APIView):
    """
    List all accounts in the system
    """
    def get(self, request: HttpRequest, format=None):
        accounts = models.Account.objects.all()
        s = serializers.AccountSerializer(accounts, many=True)
        return Response(s.data)

    def post(self, request: HttpRequest, format=None):
        data = JSONParser().parse(request)
        s = serializers.AccountSerializer(data=data)
        if not s.is_valid():
            return Response(s.errors, status=HTTP_400_BAD_REQUEST)

        s.save()
        return Response(s.data, status=HTTP_201_CREATED)


class DetailAccounts(APIView):
    """
    Show detail relating to a specific account
    """
    def get(self, request: HttpRequest, pk: int, format=None):
        account = models.Account.objects.get(pk=pk)
        s = serializers.AccountSerializer(account)
        return Response(s.data)

    def delete(self, request: HttpRequest, pk: int, format=None):
        account = models.Account.objects.get(pk=pk)
        account.active = False
        account.save()
        return Response(serializers.AccountSerializer(account).data)

class DetailAccountUpdate(APIView):
    """
    Activate/Deactivate a specific account
    """
    def get(self, request: HttpRequest, pk: int, action: str = 'activate', format=None):
        if action not in ('activate', 'deactivate'):
            return Response(status=HTTP_400_BAD_REQUEST)

        account = models.Account.objects.get(pk=pk)
        account.active = action == 'activate'
        account.save()
        return Response(serializers.AccountSerializer(account).data, status=HTTP_202_ACCEPTED)


def get_pk_value(kwargs, *keys):
    # print('searching')
    # print(kwargs)
    # print('for', keys)
    for k in keys:
        if k in kwargs:
            return kwargs[k]
        if f'{k}_pk' in kwargs:
            return kwargs[f'{k}_pk']

    return kwargs.get('pk', None)

class ListResource(ListResourceMixin, APIView):
    """
    Lists objects of a particular resource type
    """
    resource = None # URL router should specify the model to use
    parent = None # For resources that only exist as a child of another
    serializer = None # Serializer must be specified
    def get(self, request: HttpRequest, format=None, **kwargs) -> HttpResponse:
        if self.parent is not None:
            # A child resource is being requested
            child = getattr(self.parent.objects.get(pk=get_pk_value(kwargs, self.parent.__name__.lower())), f'{self.resource.__name__.lower()}_set')
            r = child.all()
        else:
            r = self.resource.objects.all()

        s = self.serializer(r, many=True)
        return Response(s.data)

    def post(self, request: HttpRequest, format=None, **kwargs) -> HttpResponse:
        # Check to see if this is supposed to be the creation of a child
        s = self._parse_and_deserialize(request, **kwargs)
        if not s.is_valid():
            return Response(s.errors, status=HTTP_400_BAD_REQUEST)
        s.save()
        return Response(s.data, status=HTTP_201_CREATED)

class DetailResource(APIView):
    resource = None
    serializer = None
    def __init__(self, resource=None, serializer=None, **kwargs):
        super().__init__(**kwargs)
        self.resource = resource
        self.serializer = serializer
        

    def get(self, request: HttpRequest, pk: int, format=None, **kwargs) -> HttpResponse:
        r = self.resource.objects.get(pk=pk)
        s = self.serializer(r)
        return Response(s.data)



class ListCorpsMembers(ListResource):
    """
    List all corps members
    """
    resource = models.CorpsMember
    serializer = serializers.CorpsMemberSerializer

class ListCorpsMemberPhones(ListResource):
    """
    List phone numbers of corps members
    """
    resource = models.CorpsMemberPhoneNumber
    parent = models.CorpsMember
    serializer = serializers.CorpsMemberPhoneSerializer

class ListCorpsMemberEmails(ListResource):
    """
    List emails of corps members
    """
    resource = models.CorpsMemberEmail
    parent = models.CorpsMember
    serializer = serializers.CorpsMemberEmailSerializer


class ListLocations(ListResource):
    """
    Lists locations needing assistance
    """
    resource = models.Location
    serializer = serializers.LocationSerializer


class ListLocationContacts(ListResource):
    """
    Lists location contacts
    """
    resource = models.LocationContact
    parent = models.Location
    serializer = serializers.LocationContactsSerializer


class ListLocationContactPhones(ListResource):
    """
    List phone numbers of location contacts
    """
    resource = models.LocationContactPhoneNumber
    parent = models.LocationContact
    serializer = serializers.LocationContactPhoneSerializer

class ListLocationContactEmails(ListResource):
    """
    List emails of location contacts
    """
    resource = models.LocationContactEmail
    parent = models.LocationContact
    serializer = serializers.LocationContactEmailSerializer

class ListDeployments(ListResource):
    """
    List deployments underway
    """
    resource = models.Deployment
    serializer = serializers.DeploymentSerializer

class ListLocationDeployments(ListResource):
    """
    List deployments underway
    """
    resource = models.Deployment
    parent = models.Location
    serializer = serializers.DeploymentSerializer

class ListAssignments(ListResource):
    """
    List all assignments, regardless of member or deployment
    """
    resource = models.Assignment
    serializer = serializers.AssignmentSerializer

class ListCorpsMemberAssignments(ListResource):
    """
    List assignments for corpmembers
    """
    resource = models.Assignment
    parent = models.CorpsMember
    serializer = serializers.AssignmentSerializer

class ListDeploymentAssignments(ListResource):
    """
    For a given deployment, list corpsmembers assigned
    """
    resource = models.Assignment
    parent = models.Deployment
    serializer = serializers.AssignmentSerializer
