import logging

from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.data_graph.models.Graph import Graph
from apps.data_graph.serializers.GraphSerializer import GraphSerializer
from apps.data_graph.views.GraphModelView import \
    CopyGraphModelsFromTemplatesView
from apps.data_graph.views.GraphRelationView import \
    CopyGraphRelationsFromTemplatesView

logger = logging.getLogger(__name__)


class GraphViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (JWTAuthentication,)
    serializer_class = GraphSerializer
    queryset = Graph.objects.all()
    model = Graph

    def list(self, request):
        user = self.request.user
        queryset = Graph.objects.filter(user=user)
        serializer = GraphSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = self.request.user
        serializer = GraphSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        graph_id = str(serializer.data['id'])
        # print(serializer.data['id'])
        # serializer.save()

        try:
            # create init models for graph '/graph/model/copy-templates/{graph_id}'
            factory = APIRequestFactory()
            req = factory.get('/graph/model/copy-templates/' + graph_id)
            force_authenticate(req, user=user)
            view = CopyGraphModelsFromTemplatesView.as_view()
            res = view(req, graph_id=graph_id)
        except Exception as e:
            logger.error('Models copying failed %s' % str(e))

        try:
            # create init relations for graph '/graph/relation/copy-templates/{graph_id}'
            factory = APIRequestFactory()
            req = factory.get('/graph/relation/copy-templates/' + graph_id)
            force_authenticate(req, user=user)
            view = CopyGraphRelationsFromTemplatesView.as_view()
            res = view(req, graph_id=graph_id)
        except Exception as e:
            logger.error('Relations copying failed %s' % str(e))

        queryset = Graph.objects.get(pk=graph_id)
        serializer = GraphSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = self.request.user
        graph = Graph.objects.get(pk=pk)
        if (user != graph.user):
            raise Exception("Yuo are not a graph owner")
        serializer = GraphSerializer(graph)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data)

    # def partial_update(self, request, pk=None):
    #     pass

    def destroy(self, request, pk=None):
        user = self.request.user
        Graph.objects.get(pk=pk).delete()
        queryset = Graph.objects.filter(user=user)
        serializer = GraphSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
