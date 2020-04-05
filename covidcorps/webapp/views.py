from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Account
from .serializers import AccountSerializer

from typing import ClassVar

# TYPE CHECKING ONLY!
from rest_framework.serializers import Serializer
from django.db.models import Model


def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")

# Standardized Responses
def json_response(serializer: ClassVar[Serializer], instance: Model) -> JsonResponse:
    s = serializer(instance)
    return JsonResponse(s.data)

def json_parse_and_save(request, serializer: ClassVar[Serializer], instance: Model = None, ok_code: int = 201, err_code: int = 400) -> JsonResponse:
    data = JSONParser().parse(request)
    if instance is None:
        s = serializer(data=data)
    else:
        s = serializer(instance, data=data)
    
    if s.is_valid():
        s.save()
        return JsonResponse(s.data, status=ok_code)
    return JsonResponse(s.errors, status=err_code)

# Handlers
def account_all(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(serializer.data, safe=False)

def account_create(request):
    return json_parse_and_save(
        request,
        serializer=AccountSerializer,
        ok_code=201,
        err_code=400,
    )


def account_get(request, account: Account):
    return json_response(AccountSerializer, account)

def account_update(request, account: Account):
    return json_parse_and_save(
        request,
        serializer=AccountSerializer,
        instance=account,
        ok_code=200,
        err_code=400,
    )

def account_delete(request, account: Account):
    account.delete()
    return HttpResponse(status=204)

# Routers
@csrf_exempt
def account_list(request):
    """
    List accounts, or create new account
    """
    return {
        'GET': account_all,
        'POST': account_create,
    }[request.method](request)

@csrf_exempt
def account_detail(request, pk):
    """
    Account detail operations
    """
    try:
        account = Account.object.get(pk=pk)
    except Account.DoesNotExist:
        return HttpResponse(status=404)

    return dict(
        GET=account_get,
        PUT=account_update,
        DELETE=account_delete,
    )[request.method](request, account)


