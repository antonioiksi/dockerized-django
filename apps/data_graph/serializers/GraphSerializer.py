from rest_framework import serializers

from apps.data_graph.models.Graph import Graph


class GraphSerializer(serializers.ModelSerializer):
    graphdata_count = serializers.IntegerField(
        source='graphdata_set.count',
        read_only=True
    )

    class Meta:
        model = Graph
        fields = ('id', 'name', 'user', 'graphdata_count')
        read_only_fields = ['user']
