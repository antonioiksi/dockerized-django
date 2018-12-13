from django.contrib.postgres.fields import ArrayField
from django.db import models


class MappingType(models.Model):
    """
    Define type of mapping for different Search System or simply data.

    For example ElasticSearch 5.6

    """
    title = models.CharField(u'Title', unique=True, null=False, blank=False, max_length=100)
    description = models.TextField(u'Description', max_length=500)
    endpoint = models.URLField(u'Endpoint', null=False, blank=True, help_text=u'without tail slash (/), for ex:http://127.0.0.1' )
    active = models.BooleanField(u'Active', null=False, blank=False, default=False)

    def __str__(self):
        return "Title: %s" % (self.title)

    class Meta:
        verbose_name = 'MappingType'
        verbose_name_plural = 'MappingTypes'
        ordering = ('title',)


class Attribute(models.Model):
    """
    This is search system layer.

    we do search through this attributes,
    for example: ElasticSearch has index field 'person_name'
    that means we are able to add attribute 'person_name' and
    do search by this field

    """

    mapping_type = models.ForeignKey('attribute.MappingType', on_delete=models.CASCADE, blank=True, null=True, )    #
    name = models.CharField(u'Name', null=False, blank=False, max_length=100)
    # title = models.CharField(u'Title', unique=True, null=False, blank=False, max_length=100)
    entity_attribute = models.ForeignKey('attribute.EntityAttribute', on_delete=models.CASCADE, blank=True, null=True, )

    def __str__(self):
        return "Mapping type: %s, Name: %s" % (self.mapping_type.title, self.name)

    class Meta:
        unique_together = ('mapping_type', 'name',)

        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
        ordering = ('mapping_type', 'name',)


class EntityAttribute(models.Model):
    """
    This is business layer

    For example 'phone', 'address'...
    Important not 'person_phone' or 'company_phone'
    The number of entity attributes must be not much,
    the smaller is the better

    """
    name = models.CharField(u'Name', unique=True, null=False, blank=False, max_length=100)
    title = models.CharField(u'Title', unique=True, null=False, blank=False, max_length=100)
    order = models.IntegerField(u'Order', null=False, blank=False, default=0)
    # attributes = ArrayField(models.CharField(max_length=100))
    # attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        return "Entity attribute %s" % self.title

    class Meta:
        verbose_name = 'Entity attribute'
        verbose_name_plural = 'Entity attributes'
        ordering = ('title',)
