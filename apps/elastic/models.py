from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

class QueryTemplate(models.Model):
    """
    Log Model
    Defines the attributes of a log
    """
    user = models.ForeignKey('auth.User',null=True, blank=True, default=None)
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    title = models.CharField(u'Title', blank=False, null=False, max_length=100)
    template = JSONField(blank=True, null=True, verbose_name="JSON template")

    class Meta:
        verbose_name = 'querytemplate'
        verbose_name_plural = 'querytemplates'
