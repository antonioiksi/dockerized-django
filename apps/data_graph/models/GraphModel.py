from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.data_graph.models.Graph import Graph
from apps.data_graph.models.GraphModelDrawing import GraphModelDrawing


class GraphModel(models.Model):
    """
    Graph Model
    """
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, blank=False, null=False,)
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    fields = ArrayField(models.CharField(max_length=100), blank=False)  # array of fields names
    is_group = models.BooleanField(u'Is group', null=False, blank=False, default=False)
    drawing = models.ForeignKey(GraphModelDrawing, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Graph model'
        verbose_name_plural = 'Graph models'

    def __str__(self):
        return self.name
