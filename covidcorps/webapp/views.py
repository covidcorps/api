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
        data = JSONParser().parse(request)
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
        if s.is_valid():
            s.save()
            return Response(s.data, status=HTTP_201_CREATED)
        return Response(s.errors, status=HTTP_400_BAD_REQUEST)


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
            child = getattr(self.parent.objects.get(pk=kwargs['pk']), f'{self.resource.__name__.lower()}_set')
            r = child.all()
        else:
            r = self.resource.objects.all()

        s = self.serializer(r, many=True)
        return Response(s.data)

    def post(self, request: HttpRequest, format=None, **kwargs) -> HttpResponse:
        s = self._parse_and_deserialize(request)
        if s.is_valid():
            s.save()
            return Response(s.data, status=HTTP_201_CREATED)
        return Response(s.errors, status=HTTP_400_BAD_REQUEST)


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
    List phone numbers of corps members
    """
    resource = models.CorpsMemberEmail
    parent = models.CorpsMember
    serializer = serializers.CorpsMemberEmailSerializer