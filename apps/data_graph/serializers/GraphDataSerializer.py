from rest_framework import serializers

from apps.data_graph.models.GraphData import GraphData


class GraphDataSerializer(serializers.ModelSerializer):
    #graph = GraphSerializer()

    class Meta:
        model = GraphData
        fields = ('id', 'data',)
