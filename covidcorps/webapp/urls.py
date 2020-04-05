from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='registration'),
    # path('accounts/', views.account_list),
    # path('accounts/<int:pk>', views.account_detail),
]