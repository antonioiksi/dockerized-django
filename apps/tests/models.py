from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.
class Test(models.Model):
    """
    Test Model
    Defines the attributes of a log
    """
    datetime = models.DateTimeField(u'ДатаВремя', auto_now_add=True)
    text = models.CharField(u'Текст', blank=False, null=False, max_length=100)

    def save(self, *args, **kwargs):
        super(Test, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
