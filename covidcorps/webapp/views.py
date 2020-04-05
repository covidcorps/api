from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Account
from .serializers import AccountSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")


# Handlers
def account_list_all(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(serializer.data, safe=False)

def account_create(request):
    data = JSONParser().parse(request)
    serializer = AccountSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=401)

# Routers
@csrf_exempt
def account_list(request):
    """
    List accounts, or create new account
    """
    return {
        'GET': account_list_all,
        'POST': account_create,
    }[request.method](request)


