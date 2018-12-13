from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.
class Log(models.Model):
    """
    Log Model
    Defines the attributes of a log
    """
    user = models.ForeignKey('auth.User', null=True, blank=True, default=None)
    ip = models.CharField(u'IP', blank=False, null=False, max_length=100)
    datetime = models.DateTimeField(u'ДатаВремя', auto_now_add=True)
    query = JSONField(blank=True, null=True, verbose_name="JSON запрос")
    event = models.CharField(u'Событие', blank=False, null=False, max_length=100)
    method = models.CharField(u'Method', blank=False, null=False, max_length=100, default='GET')
    duration = models.DurationField(u'Продолжительность', null=True, blank=True, default=None)

    def get_event(self):
        return 'Log belongs to ' + self.event + ' events.'

    def __str__(self):
        return "Событие %s: ДатаВремя %s" % (self.event, self.datetime)

    def save(self, *args, **kwargs):
        super(Log, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
