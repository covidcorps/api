from django.http import HttpResponse, JsonResponse, HttpRequest
from .serializers import AccountSerializer
from .models import Account

from rest_framework.parsers import JSONParser

# Type checking only
from typing import ClassVar
from rest_framework.serializers import Serializer
from django.db.models import Model

# Standardized Responses
def json_response(serializer: ClassVar[Serializer], instance: Model) -> JsonResponse:
    s = serializer(instance)
    return JsonResponse(s.data)

def json_parse_and_save(request: HttpRequest, serializer: ClassVar[Serializer], instance: Model = None, ok_code: int = 201, err_code: int = 400) -> JsonResponse:
    data = JSONParser().parse(request)
    if instance is None:
        s = serializer(data=data)
    else:
        s = serializer(instance, data=data)
    
    if s.is_valid():
        s.save()
        return JsonResponse(s.data, status=ok_code)
    return JsonResponse(s.errors, status=err_code)

# Accounts
def account_all(request: HttpRequest):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(serializer.data, safe=False)

def account_create(request: HttpRequest):
    return json_parse_and_save(
        request,
        serializer=AccountSerializer,
        ok_code=201,
        err_code=400,
    )


def account_get(request: HttpRequest, account: Account):
    return json_response(AccountSerializer, account)

def account_update(request: HttpRequest, account: Account):
    return json_parse_and_save(
        request,
        serializer=AccountSerializer,
        instance=account,
        ok_code=200,
        err_code=400,
    )

def account_delete(request: HttpRequest, account: Account):
    account.delete()
    return HttpResponse(status=204)