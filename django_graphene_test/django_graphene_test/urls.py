"""
URL configuration for django_graphene_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from bank.schema import schema
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from bank.views import UserViewSet, TransactionHistoryViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"transaction_history", TransactionHistoryViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("api/", include(router.urls)),
]
