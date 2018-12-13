from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied

from apps.data_bin.models import Bin, BinItem
from apps.data_bin.serializers import (BinItemSerializer,
                                       BinItemSimpleSerializer)


class UserItemsView(generics.ListAPIView):
    """
    Return all items from all user's bins
    """
    serializer_class = BinItemSimpleSerializer
    #permission_classes = (IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        bin_items = BinItem.objects.filter(bin__user=user).exclude(query__isnull=True).exclude(query__exact={}).order_by('-datetime')
        return bin_items



class BinItemListView(generics.ListAPIView):
    """
    Return list from 'BinItem's by Bin's ID
    """
    serializer_class = BinItemSimpleSerializer
    #permission_classes = (IsAdminUser,)

    def get_queryset(self):
        bin_pk = self.kwargs['bin_pk']
        user = self.request.user
        try:
            bin = Bin.objects.get(pk=bin_pk, user=user)
        except Bin.DoesNotExist:
            raise NotFound(detail='Object Bin not found', code=None)

        # if user != bin.user:
        #    raise PermissionDenied(detail='You do not have access to this Bin object', code=None)
        return BinItem.objects.filter(bin=bin)


class BinItemDeleteView(generics.DestroyAPIView):
    """
    Remove 'Bin Item' by ID
    """
    serializer_class = BinItemSerializer

    def perform_destroy(self, instance):
        instance.delete()


class BinItemView(generics.RetrieveAPIView):
    """
    Return 'Bin' list for current user
    """
    serializer_class = BinItemSerializer
    #permission_classes = (IsAdminUser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = self.request.user
        queryset = BinItem.objects.all()
        binItem = get_object_or_404(queryset, pk=pk)# BinItem.objects.get(pk=pk)

        # check user
        if user != binItem.bin.user:
            raise Http404("No BinItem matches the given query.")
        #queryset = BinItem.objects.all()
        #bin_item = get_object_or_404(queryset, pk=pk)
        #BinItem.objects.filter(pk=pk)
        return BinItem.objects.filter(pk=pk)


class BinItemFlatView(generics.RetrieveAPIView):
    """
    Return 'Bin' list for current user
    """
    serializer_class = BinItemSerializer
    #permission_classes = (IsAdminUser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = self.request.user
        queryset = BinItem.objects.all()
        binItem = get_object_or_404(queryset, pk=pk)# BinItem.objects.get(pk=pk)

        # check user
        if user != binItem.bin.user:
            raise Http404("No BinItem matches the given query.")
        #queryset = BinItem.objects.all()
        #bin_item = get_object_or_404(queryset, pk=pk)
        #BinItem.objects.filter(pk=pk)
        return BinItem.objects.filter(pk=pk)
