from rest_framework import serializers

from apps.data_graph.models.GraphModel import GraphModel
from apps.data_graph.serializers.GraphModelDrawingSerializer import \
    GraphModelDrawingSimpleSerializer


class GraphModelSerializer(serializers.ModelSerializer):
    #graph = GraphSerializer()
    drawing = GraphModelDrawingSimpleSerializer()

    class Meta:
        model = GraphModel
        fields = ('id', 'name', 'graph', 'fields', 'is_group', 'drawing', )


class GraphModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphModel
        fields = ('name',)

class GraphModelCreateSerializer(serializers.ModelSerializer):
    # graph = GraphSerializer()
    # drawing = GraphModelDrawingSimpleSerializer()

    class Meta:
        model = GraphModel
        fields = ('id', 'name', 'graph', 'fields', 'is_group', 'drawing', )
