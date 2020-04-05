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
from rest_framework.views import APIView

from . import handlers
from .models import Account
from .serializers import AccountSerializer


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
#     serializer = AccountSerializer




class ListAccounts(APIView):
    """
    List all accounts in the system
    """
    def get(self, request, format=None):
        accounts = Account.objects.all()
        s = AccountSerializer(accounts, many=True)
        return Response(s.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        s = AccountSerializer(data=data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=HTTP_201_CREATED)
        return Response(s.errors, status=HTTP_400_BAD_REQUEST)


class DetailAccounts(APIView):
    """
    Show detail relating to a specific account
    """
    def get(self, request, pk, format=None):
        account = Account.objects.get(pk=pk)
        s = AccountSerializer(account)
        return Response(s.data)
