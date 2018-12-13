from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.data_graph.models.GraphModelDrawing import GraphModelDrawing


class ModelTemplate(models.Model):
    """
    ModelTemplate Model
    """
    user = models.ForeignKey('auth.User', null=True, blank=True, default=None)
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    fields = ArrayField(models.CharField(max_length=100), blank=False)  # array of fields names
    is_group = models.BooleanField(u'Is group', null=False, blank=False, default=False)  # simplify drawing
    drawing = models.ForeignKey(GraphModelDrawing, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Model template'
        verbose_name_plural = 'Model templates'

    def __str__(self):
        return self.name
