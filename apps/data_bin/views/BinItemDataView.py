import json

from rest_framework import generics, status, views, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_bin.models import Bin, BinItem
from apps.data_bin.utils import flatten


class BinItemDataView(views.APIView):
    """
    Get data from Items by Bin's Id (flat json mode)
    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        bin_pk = self.kwargs['bin_pk']

        try:
            bin = Bin.objects.get(pk=bin_pk)
        except:
            return Response({'status':'error', 'message': 'bin with id: %s not found or not access' % bin_pk}, status=status.HTTP_400_BAD_REQUEST)
        bin_items = BinItem.objects.filter(bin=bin)

        _ids = []
        result = []

        # distinct json
        for itemData in bin_items:
            item_id = itemData.id
            for item in itemData.data:
                _id = item['_id']

                if _id not in _ids:
                    item['_item_id'] = item_id
                    item['_json_query'] = itemData.query
                    result.append(item)
                    _ids.append(_id)
            # allData.extend(itemData.data)

        # flatten json
        # flatData = [
        #    flatten(data)
        #    for data in allData]
        # list = [
        # {'_id':item['_id'] for item in binItem.data}
        # binItem.data
        #    for binItem in BinItem.objects.filter(bin=bin)]

        # temp = [{'_id':1,'name':'n1'},{'_id':2,'name':'n2'}]

        return Response(result, status=status.HTTP_200_OK)


class FlatDataBinView(views.APIView):
    """
    Get data from Items by Bin's Id (flat json mode)
    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        queryset = Bin.objects.all()
        user = self.request.user
        pk = self.kwargs['pk']
        bin = Bin.objects.get(pk=pk)

        # if user!=bin.user:
        #    return Response({'error':'you are not a bin\'s owner!'}, status=status.HTTP_403_FORBIDDEN)

        ids = []
        allData = []

        # distinct json
        for itemData in BinItem.objects.filter(bin=bin):
            for item in itemData.data:
                id = item['_id']
                if id not in ids:
                    allData.append(item)
                    ids.append(id)
            # allData.extend(itemData.data)

        # flatten json
        flatData = [
            flatten(data)
            for data in allData]
        # list = [
        # {'_id':item['_id'] for item in binItem.data}
        # binItem.data
        #    for binItem in BinItem.objects.filter(bin=bin)]

        # temp = [{'_id':1,'name':'n1'},{'_id':2,'name':'n2'}]

        return Response(flatData, status=status.HTTP_200_OK)
        # return Response(temp, status=status.HTTP_200_OK)


class RemoveRowFromDataView(views.APIView):
    """
    Remove row from json array BinItem.data by "_id"
    """

    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.request.user
        keys = json.loads(request.body.decode("utf-8"))
        for key in keys:
            arr_key = key.split('_')
            item_id = arr_key[0]
            id = str( arr_key[1])

            try:
                bin_item = BinItem.objects.get(pk=item_id, bin__user=user)

            except Bin.DoesNotExist:
                raise NotFound(detail='Object Bin not found', code=None)

            bin_item.data = [row for row in bin_item.data if str(row['_id']) != id]
            bin_item.save()

        return Response(None, status=status.HTTP_200_OK)
