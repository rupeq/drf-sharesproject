from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


class CurrencyTable(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        curobj = Currency.objects.all()
        serializer = CurrencySerializer(curobj, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        curobj = Currency.objects.all()
        curobj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrencyUpdateDelete(APIView):
    permission_classes = (IsAdminUser, )

    def get_object(self, id, *args, **kwargs):
        try:
            return Currency.objects.get(id=id)
        except Currency.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id, *args, **kwargs):
        curobj = self.get_object(id)
        serializer = CurrencySerializer(curobj)
        return Response(serializer.data)

    def put(self, request, id, *args, **kwargs):
        curobj = self.get_object(id)
        serializer = CurrencySerializer(curobj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        curobj = self.get_object(id)
        curobj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


