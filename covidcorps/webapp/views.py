from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import Template

from .models import Account

from . import handlers

# TYPE CHECKING ONLY!
from django.db.models import Model
from typing import ClassVar, Optional, List


def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")


def get_or_error(cls: ClassVar[Model], pk) -> Optional[Model]:
    try:
        return cls.object.get(pk=pk), None
    except cls.DoesNotExist:
        return None, HttpResponse(status=404)

# Account Views
@csrf_exempt
def account_list(request: HttpRequest) -> HttpResponse:
    """
    List accounts, or create new account
    """
    return dict(
        GET=handlers.account_all,
        POST=handlers.account_create,
    )[request.method](request)

@csrf_exempt
def account_detail(request, pk) -> HttpResponse:
    """
    Account detail operations
    """
    account, err_response = get_or_error(Account, pk)
    if err_response:
        return err_response

    return dict(
        GET=handlers.account_get,
        PUT=handlers.account_update,
        DELETE=handlers.account_delete,
    )[request.method](request, account)


# Location Views
def locations_index(request: HttpRequest) -> HttpResponse:
    """
    Index views
    """

def locations_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Detail views
    """

# Deployments
def deployments_index(request: HttpRequest) -> HttpResponse:
    """
    Deployments index views
    """

def deployments_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Deployments detail views
    """

# Assignments
def assignments_index(request: HttpRequest) -> HttpResponse:
    """
    Assignments index views
    """

def assignments_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Assignments detail views
    """

# Registration
def unwrap(d, *keys) -> List:
    return tuple(d.get(k) for k in keys)


@csrf_exempt
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request,'webapp/register.html', {})

    username, pw = unwrap(request.POST, 'username', 'password')
    user = Account.objects.create_user(username=username, password=pw)
    user.save()
    return redirect('/auth/login')

