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
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView, get_view_name
from rest_framework.serializers import Serializer

from . import handlers, models, serializers

import io

RESOURCE_MODEL_MAP = dict(
    accounts=(models.Account, serializers.AccountSerializer),
    corpsmembers=(models.CorpsMember, serializers.CorpsMemberSerializer),
    phones=(models.CorpsMemberPhoneNumber, serializers.CorpsMemberPhoneSerializer),
    emails=(models.CorpsMember, serializers.CorpsMemberEmailSerializer),
    locations=(models.Location, serializers.LocationSerializer),
    contacts=(models.LocationContact, serializers.LocationContactsSerializer),
    deployments=(models.Deployment, serializers.DeploymentSerializer),
    assignments=(models.Assignment, serializers.AssignmentSerializer),
)

def parse_incoming(request: HttpRequest):
    """
    Parses the incoming JSON data stream to a dict that can be read by
    the serializer
    """
    if not isinstance(request.data, dict):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
    else:
        data = request.data
    
    return data

def serializer_update(method: str, data, inst, serializer, **kwargs):
    if method == 'POST':
        s = serializer(data=data)
    elif method == 'PUT':
        s = serializer(inst, data=data)
    
    if not s.is_valid():
        return Response(s.errors, status=HTTP_400_BAD_REQUEST)

    s.save()
    return Response(s.data, status=HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def api_handler(request: HttpRequest, **kwargs):
    pfx = '/webapp/'
    path = request.path[len(pfx):] if request.path.startswith(pfx) else request.path # Strip away the app name, if present
    path = path[:-1] if request.path.endswith('/') else path # Strip away a trailing slash, if present
    path_parts = path.split('/')
    try:
        # Check the last element of the path. If an int, then this should be routed to the detail handler
        pk = int(path_parts[-1])
        resource = path_parts[-2]
        return detail_handler(request, resource, pk, **kwargs)
    except ValueError:
        # Route to the list handler
        if request.method not in ('GET', 'POST'):
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        return list_handler(request, path_parts, **kwargs)

def list_handler(request: HttpRequest, path_parts, **kwargs):
    # Now for each part of the path, we want to find the matching model)
    base_model, _ = RESOURCE_MODEL_MAP.get(path_parts[0]) # Model associated with base resource in path will be stored here
    rv = base_model.objects
    if len(path_parts) > 1:
        # Being asked for a nested resource
        for part in path_parts[1:]:
            try:
                # If we're able to extract an integer, then we have a PK and need to use .get to retrieve
                pk = int(part)
                rv = rv.get(pk=pk)
            except ValueError:
                # Not a pk, so we need to find the associated items
                try:
                    rv = getattr(rv, part)
                except AttributeError:
                    # This happens when the relationship key on the model uses the _set naming convention
                    rv = getattr(rv, f'{part[:-1]}_set')
        
    # Once here, rv should be set to the final resource in the path
    _, serializer = RESOURCE_MODEL_MAP.get(path_parts[-1])
    if request.method == 'POST':
        # If this is a POST need to create a new resource.
        return serializer_update(request.method, parse_incoming(request), rv, serializer, **kwargs)

    # GET request, so now we just need to use all() to get all the instances of the resource and return that
    rv = rv.all()
    s = serializer(rv, many=True)
    return Response(s.data)

def detail_handler(request: HttpRequest, resource, pk, **kwargs):
    model, serializer = RESOURCE_MODEL_MAP.get(resource)

    # Get the object associated with the primary key and resource name
    r = model.objects.get(pk=pk)

    # If this is a PUT or PATCH, use the update function to parse the data and update the instance
    if request.method in ('PUT', 'PATCH'):
        return serializer_update(request.method, parse_incoming(request), r, serializer, **kwargs)
    
    # Otherwise just return the relevant resource
    s = serializer(r)
    return Response(s.data)



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





class ManyResource(APIView):
    # /corpsmembers/1/phones
    def get(self, request: HttpRequest, format=None, hydrate=False, **kwargs):
        # First we need to break the path into pieces to figure out what's being requested
        path = request.path.lstrip('/webapp/')
        path_parts = path.split('/')

        # Now for each part of the path, we want to find the matching model)
        base_model, _ = RESOURCE_MODEL_MAP.get(path_parts[0]) # Model associated with base resource in path will be stored here
        rv = base_model.objects
        if len(path_parts) > 1:
            # Being asked for a nested resource
            for part in path_parts[1:]:
                try:
                    # If we're able to extract an integer, then we have a PK and need to use .get to retrieve
                    pk = int(part)
                    rv = rv.get(pk=pk)
                except ValueError:
                    # Not a pk, so we need to find the associated items
                    try:
                        rv = getattr(rv, part)
                    except AttributeError:
                        # This happens when the relationship key on the model uses the _set naming convention
                        rv = getattr(rv, f'{part[:-1]}_set')
            
        # Once here, rv should be set to the final resource in the path, so now we just need to
        # use all() to get all the instances of the resource and return that
        rv = rv.all()
        _, serializer = RESOURCE_MODEL_MAP.get(path_parts[-1])
        s = serializer(rv, many=True)
        return Response(s.data)




        





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


class CorpsMemberDetailHydrated(APIView):
    def get(self, request: HttpRequest, pk: int, format=None, **kwargs) -> HttpResponse:
        if request.GET.get('hydrate') is None:
            r = models.CorpsMember.objects.get(pk=pk)
            return Response(serializers.CorpsMemberSerializer(r).data)

        q = models.CorpsMember.objects.filter(id=pk).prefetch_related('deployments')
        r = q[0]
        r.assignments = r.assignment_set.all()
        s = serializers.CorpsMemberHydratedSerializer(r)
        return Response(s.data)


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