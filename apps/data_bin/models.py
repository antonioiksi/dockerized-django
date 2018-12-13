import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

logger = logging.getLogger(__name__)

class Bin(models.Model):

    class Meta:
        unique_together = ('user', 'name',)

    """
    Case Model
    Defines the attributes of a case
    """
    user = models.ForeignKey('auth.User', null=True, blank=True, default=None)
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    active = models.BooleanField(u'Active', null=False, blank=False, default=False)

    def __str__(self):
        return "Bin %s: user %s" % (self.name, self.user)



class BinItem(models.Model):
    """
    Case Model
    Defines the attributes of a case
    """
    bin = models.ForeignKey('Bin', on_delete=models.CASCADE, blank=False, null=False, )
    url = models.CharField(u'url', blank=False, null=False, max_length=2000)
    query = JSONField(blank=True, null=True, verbose_name="query")
    data = JSONField(blank=False, null=False, verbose_name="data")
    mapping = JSONField(blank=True, null=True, verbose_name="mapping")
    datetime = models.DateTimeField(u'datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Bin Item'
        verbose_name_plural = 'Bin Items'
