from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


# Create your models here.
class Graph(models.Model):
    """
    Graph object
    """
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    user = models.ForeignKey('auth.User',null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Graph'
        verbose_name_plural = 'Graph list'

    def __str__(self):
        return self.name
