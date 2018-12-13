import json
from pprint import pprint

from django.shortcuts import render
from rest_framework import status, views
# Create your views here.
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_bin.views.BinItemDataView import FlatDataBinView
from apps.data_bin.views.FlatExtendAttributeDataBinView import \
    FlatExtendAttributeDataBinView
from apps.data_bin.views.FlatExtendEntityAttributeDataBinView import \
    FlatExtendEntityAttributeDataBinView
from apps.data_graph.models.Graph import Graph
from apps.data_graph.models.GraphData import GraphData


class LoadGraphFromBinView(views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        bin_pk = self.kwargs['bin_pk']
        graph_pk = self.kwargs['graph_pk']

        graph = Graph.objects.get(pk=graph_pk)

        user = self.request.user
        factory = APIRequestFactory()
        req = factory.get('/bin/flat-data/' + bin_pk)
        force_authenticate(req, user=user)

        view = FlatDataBinView.as_view()
        res = view(req, pk=bin_pk)
        # pprint(json.loads( resp.body))

        for item in res.data:
            graphData = GraphData(graph=graph, data=item)
            graphData.save()

        return Response([len(res.data)], status=status.HTTP_200_OK)


class LoadExtendGraphFromBinView(views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        bin_pk = self.kwargs['bin_pk']
        graph_pk = self.kwargs['graph_pk']

        graph = Graph.objects.get(pk=graph_pk)

        user = self.request.user
        factory = APIRequestFactory()
        req = factory.get('/bin/flat-extend-data/' + bin_pk)
        force_authenticate(req, user=user)

        view = FlatExtendEntityAttributeDataBinView.as_view()
        res = view(req, pk=bin_pk)
        # pprint(json.loads( resp.body))

        for item in res.data:
            graphData = GraphData(graph=graph, data=item)
            graphData.save()

        return Response([len(res.data)], status=status.HTTP_200_OK)
