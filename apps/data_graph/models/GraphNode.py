from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.data_graph.models.Graph import Graph


class GraphNode(models.Model):
    """
    """
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, blank=False, null=False,)
    #model = models.ForeignKey('data_graph.GraphModel', on_delete=models.CASCADE, blank=False, null=False)
    #graph_data = models.ForeignKey('data_graph.GraphData', on_delete=models.CASCADE, blank=False, null=False)
    node_json = JSONField(blank=False, null=False, verbose_name="Node json")


class GraphNodeEdge(models.Model):
    """
    """
    #class Meta:
        # делает уникальным направление обмена
    #    unique_together = ("from_node", "to_node")

    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, blank=False, null=False,)
    #relation = models.ForeignKey('data_graph.GraphRelation', on_delete=models.CASCADE, blank=False, null=False)
    #from_node = models.ForeignKey('data_graph.GraphNode', on_delete=models.CASCADE, blank=False, null=False, related_name="from_node")
    #to_node = models.ForeignKey('data_graph.GraphNode', on_delete=models.CASCADE, blank=False, null=False, related_name="to_node")
    edge_json = JSONField(blank=False, null=False, verbose_name="Edge json")
