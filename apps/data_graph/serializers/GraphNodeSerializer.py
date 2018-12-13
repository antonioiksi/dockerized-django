from rest_framework import serializers

from apps.data_graph.models.GraphNode import GraphNode
from apps.data_graph.serializers.GraphDataSerializer import GraphDataSerializer
from apps.data_graph.serializers.GraphModelSerializer import \
    GraphModelNameSerializer


class GraphNodeSerializer(serializers.ModelSerializer):
    #model = GraphModelSerializer()
    #model = GraphModelNameSerializer()
    #graph_data = GraphDataSerializer()

    class Meta:
        model = GraphNode
        fields = ('id', 'graph', 'node_json',)


class GraphNodeJsonSerializer(serializers.ModelSerializer):

    class Meta:
        model = GraphNode
        fields = ('node_json',)
