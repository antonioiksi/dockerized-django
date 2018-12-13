# Create your models here.
from django.contrib.postgres.fields import JSONField
from django.db import models


class ElasticSettings(models.Model):
    """
    ElasticSettings Model
    Defines the attributes of a UserSettings
    """
    user = models.ForeignKey('auth.User',null=True, blank=True, default=None)
    name = models.CharField(u'Name', blank=False, null=False, max_length=100)
    title = models.CharField(u'Title', blank=False, null=False, max_length=100)
    setting = JSONField(blank=True, null=True, verbose_name="Setting")


    def get_event(self):
        return 'ElasticSettings belongs to ' + self.event + ' events.'


    def save(self, *args, **kwargs):
        super(ElasticSettings, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'ElasticSettings item'
        verbose_name_plural = 'ElasticSettings list'
