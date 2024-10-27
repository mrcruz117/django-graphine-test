from django.shortcuts import render
from rest_framework import viewsets
from .models import User, TransactionHistory
from .serializers import UserSerializer, TransactionHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionHistoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer
