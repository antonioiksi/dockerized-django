from django.contrib.postgres.fields import JSONField
from django.db import models


class GraphModelDrawing(models.Model):
    """
    Graph Model Drawing
    """
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    json = JSONField(blank=False, null=True, verbose_name="json")

    class Meta:
        verbose_name = 'Graph model drawing'
        verbose_name_plural = 'Graph model drawings'

    def __str__(self):
        return self.name
