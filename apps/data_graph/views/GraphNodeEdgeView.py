from pprint import pprint

from rest_framework import status, views
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_graph.comparators.comparators_old import (EQUAL, EQUAL_IGNORE_CASE, INCLUDE,
                                         PARTIAL_RATIO, Comparator)
from apps.data_graph.models.Graph import Graph
from apps.data_graph.models.GraphNode import GraphNode, GraphNodeEdge
from apps.data_graph.models.GraphRelation import GraphRelation


class GraphNodeEdgeClearView(views.APIView):
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        graph_id = self.kwargs['graph_id']
        user = self.request.user
        graph = Graph.objects.get(pk=graph_id)
        if user != graph.user:
            raise Exception( "You are not a graph's owner")
        deleted = GraphNodeEdge.objects.filter(graph=graph).delete()
        return Response([deleted], status=status.HTTP_200_OK)


class GraphNodeEdgeListView(views.APIView):
    """
    Return 'Bin' list for current user
    """
    #permission_classes = (IsAdminUser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        graph_id = self.kwargs['graph_id']
        user = self.request.user
        graph = Graph.objects.get(pk=graph_id)
        if user != graph.user:
            raise Exception( "You are not a graph's owner")
        #queryset = GraphNode.objects.filter(graph=graph)
        array = GraphNodeEdge.objects.values_list('edge_json', flat=True)
        #return queryset

        return Response(array, status=status.HTTP_200_OK)



class GraphNodeEdgeAddForRelationsView(views.APIView):
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        """
        Get edges for nodes
        :param request.data:
            json - array of Relation object's names, like:
            ["call_to", "same_index_type",]
        :param args:
        :param kwargs:
            graph_name - name field of Graph object
        :return:
            json array with edges like [{from: 324, to: 211},...] 344 and 211 pk from GraphNode
        """
        user = self.request.user
        graph_id = self.kwargs['graph_id']
        relation_names_json = request.data

        try:
            graph = Graph.objects.get(pk=graph_id)
        except:
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        # remove all edges
        GraphNodeEdge.objects.filter(graph=graph).delete()

        arr_data = []
        for relation_name in relation_names_json:
            relation = GraphRelation.objects.get(graph=graph, name=relation_name)

            #nodes1 = GraphNode.objects.filter(graph=graph,graph_data__data__has_keys=relation.from_fields)
            #nodes2 = GraphNode.objects.filter(graph=graph,graph_data__data__has_keys=relation.to_fields)
            #TODO здесь ошибка выдается слишком много узлов
            nodes1 = GraphNode.objects.filter(graph=graph, node_json__has_keys=relation.from_fields)
            nodes2 = GraphNode.objects.filter(graph=graph, node_json__has_keys=relation.to_fields)
            #graph_data1 = GraphData.objects.filter(data__has_keys=relation.from_fields)
            #graph_data2 = GraphData.objects.filter(data__has_keys=relation.to_fields)

            for i1 in range(len(nodes1)):
                for i2 in range(i1+1, len(nodes2)):
                    item1 = nodes1[i1]
                    item2 = nodes2[i2]
                    node1_pk = item1.node_json["id"]
                    node2_pk = item2.node_json["id"]
                    if node1_pk==node2_pk:
                        break

                    success = True
                    for i in range(len(relation.from_fields)):
                        value1 = item1.node_json[relation.to_fields[i]]
                        value2 = item2.node_json[relation.from_fields[i]]
                        comparator = relation.comparators[i]

                        if comparator.__eq__(EQUAL):
                            if not Comparator.equal(value1, value2):
                                success = False
                                break
                        elif comparator.__eq__(EQUAL_IGNORE_CASE):
                            if not Comparator.equalIgnoreCase(value1, value2):
                                success = False
                                break
                        elif comparator.__eq__(INCLUDE):
                            if not Comparator.include(value1, value2):
                                success = False
                                break
                        elif comparator.__eq__(PARTIAL_RATIO):
                            if not Comparator.partial_ratio(value1, value2):
                                success = False
                                break

                    if(success):
                        edge = {
                            'from': node1_pk, # item1.pk,
                            'to': node2_pk, #item2.pk,
                            'label': relation_name
                        }
                        arr_data.append(edge)
                        #break

        return Response(arr_data, status=status.HTTP_200_OK)
