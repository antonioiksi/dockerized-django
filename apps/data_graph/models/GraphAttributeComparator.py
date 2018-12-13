from django.db import models

# https://pypi.python.org/pypi/abydos
# https://pypi.python.org/pypi/PyICU/
from apps.data_graph.comparators import COMPARATOR_CHOICES, EQUAL

"""
class GraphAttributeComparator(models.Model):
    attribute_one = models.CharField(u'First attribute name', blank=False, null=False, max_length=100)
    attribute_two = models.CharField(u'Second attribute name', blank=False, null=False, max_length=100)
    comparator = models.CharField(
        max_length=50,
        choices=COMPARATOR_CHOICES,
        default=EQUAL,
        blank=False, null=False
    )
    #func_name = models.CharField(u'Function name', blank=False, null=False, max_length=100)

    def __str__(self):
        return "%s (%s - %s)" % (self.comparator, self.attribute_one, self.attribute_two)
"""
