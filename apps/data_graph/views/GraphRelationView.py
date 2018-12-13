from rest_framework import permissions, status, views, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_graph.models.Graph import Graph
from apps.data_graph.models.GraphNode import GraphNode, GraphNodeEdge
from apps.data_graph.models.GraphRelation import GraphRelation
from apps.data_graph.models.RelationTemplate import RelationTemplate
from apps.data_graph.serializers.GraphRelationSerializer import \
    GraphRelationSerializer


class GraphRelationForGraphViewSet(ListAPIView):
    permission_classes = (PublicEndpoint,)

    serializer_class = GraphRelationSerializer
    def get_queryset(self):
        graph_id = self.kwargs['graph_id']
        #user = self.request.user
        graph = Graph.objects.get(pk=graph_id)
        queryset = GraphRelation.objects.filter(graph=graph)
        #queryset = GraphModel.objects.all()
        return queryset


class GraphRelationViewSet(viewsets.ViewSet):
    permission_classes = (PublicEndpoint,)

    def list(self, request):
        queryset = GraphRelation.objects.all()
        serializer = GraphRelationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = self.request.user
        serializer = GraphRelationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # graph_pk = serializer.initial_data['graph']
        # graph = Graph.objects.get(pk=graph_pk)
        # queryset = GraphRelation.objects.filter(graph=graph)
        # serializer = GraphRelationSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = self.request.user
        GraphRelation.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
class GraphRelationBuilderView(views.APIView):
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        name = self.kwargs['graph_name']
        user = self.request.user
        graph = Graph.objects.get(name=name)
        if user != graph.user:
            raise Exception( "You are not a graph's owner")

        nodes = GraphNode.objects.filter(graph=graph)

        counter = {

        }

        for relation_name in request.data:
            relation = GraphRelation.objects.get(name=relation_name)

            count = 0

            for i1 in range(len(nodes)):
                for i2 in range(i1+1, len(nodes)):
                    node1 = nodes.get(i1)
                    node2 = nodes[i2]
                    if (node1.id != node2.id):
                        success = True
                        for i in range(len(relation.from_fields)):
                            val1 = node1[relation.from_fields[i]]
                            val2 = node2[relation.from_fields[i]]
                            if (val1!=val2):
                                success = False
                                break
                        if (success):
                            edge = GraphNodeEdge(
                                relation=relation,
                                from_node=node1,
                                to_node=node2,
                            )
                            edge.save()
                            count += 1
                    counter[relation_name] = count

        return Response(counter, status=status.HTTP_200_OK)
"""



class GraphRelationComparatorsView(views.APIView):
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        comparators = [
            {
                'name':'equal',
                'title':'equal'
            },
            {
                'name':'similar',
                'title':'similar'
            },
            {
                'name':'translit_similar',
                'title':'translit_similar'
            },
        ]
        return Response(comparators, status=status.HTTP_200_OK)


class CopyGraphRelationsFromTemplatesView(views.APIView):
    # adding models for graph from user's ModelTemplates
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (PublicEndpoint,)

    def get(self, request, graph_id):
        user = request.user
        # graph_id = self.kwargs['graph_id']
        graph = Graph.objects.get(pk=graph_id)

        count = 0
        countErr = 0
        userRelationTemplates = RelationTemplate.objects.filter(user=user)
        for userRelationTemplate in userRelationTemplates:
            graphRelations = GraphRelation.objects.filter(graph=graph, name=userRelationTemplate.name)
            if len(graphRelations) == 0:
                graphRelation = GraphRelation(
                    graph=graph,
                    name=userRelationTemplate.name,
                    from_fields=userRelationTemplate.from_fields[:],
                    to_fields=userRelationTemplate.from_fields[:],
                    comparators=userRelationTemplate.comparators[:]
                )
                graphRelation.save()
                count += 1

        return Response({'Created': count, 'Error': countErr}, status=status.HTTP_200_OK)
