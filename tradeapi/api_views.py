from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import *
from .serializers import *


class ItemsView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class FavoriteList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = WatchList.objects.all()
    serializer_class = FavoriteListSerializer

    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)
        item = request.data.get('item')
        favobj = WatchList(user=user, item=item)
        favobj.save()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        qs = self.queryset.filter(user=user_id)
        if qs:
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)








