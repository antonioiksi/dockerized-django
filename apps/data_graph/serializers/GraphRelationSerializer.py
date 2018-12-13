from rest_framework import serializers

from apps.data_graph.models.GraphRelation import GraphRelation


class GraphRelationSerializer(serializers.ModelSerializer):
    #graph = GraphSerializer()

    class Meta:
        model = GraphRelation
        fields = ('id', 'name', 'graph', 'from_fields', 'to_fields', 'comparators',)
