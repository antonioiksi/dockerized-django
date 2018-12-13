from django.contrib.postgres.fields import ArrayField
from django.db import models

"""
class GraphAttribute(models.Model):
    graph = models.ForeignKey('data_graph.Graph', on_delete=models.CASCADE, blank=False, null=False, primary=True)
    name = models.CharField(u'Name', blank=False, null=False, max_length=100, primary=True)

    class Meta:
        verbose_name = 'Graph Attribute'
        verbose_name_plural = 'Graph Attributes'

    def __str__(self):
        return self.name
"""
