from rest_framework import serializers

from apps.data_graph.models.GraphModelDrawing import GraphModelDrawing


class GraphModelDrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphModelDrawing
        fields = ('id', 'name', 'json',)


class GraphModelDrawingSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphModelDrawing
        fields = ('id', 'name', )
