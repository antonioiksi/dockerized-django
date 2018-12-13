from django.contrib import admin

# Register your models here.
from apps.data_graph.models.Graph import Graph
# from apps.data_graph.models.GraphAttributeComparator import GraphAttributeComparator
from apps.data_graph.models.GraphData import GraphData
from apps.data_graph.models.GraphModel import GraphModel
from apps.data_graph.models.GraphModelDrawing import GraphModelDrawing
from apps.data_graph.models.GraphNode import GraphNode
from apps.data_graph.models.GraphRelation import GraphRelation
from apps.data_graph.models.ModelTemplate import ModelTemplate
from apps.data_graph.models.RelationTemplate import RelationTemplate


class GraphAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user',)
    ordering = ('user', 'name')
    list_filter = (
        ('user'),
    )


class GraphModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'fields', 'is_group', 'drawing',)
    ordering = ('graph', 'name')
    list_filter = (
        ('graph'),
    )


class GraphRelationAdmin(admin.ModelAdmin):
    list_display = ('graph', 'name',)
    ordering = ('graph', 'name')
    list_filter = (
        ('graph'),
    )


class GraphModelDrawingAdmin(admin.ModelAdmin):
    list_display = ('name', 'json',)


class GraphDataAdmin(admin.ModelAdmin):
    list_display = ('pk', 'graph', 'data',)


class GraphNodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'graph', 'node_json',)
    ordering = ('pk',)


# class GraphAttributeComparatorAdmin(admin.ModelAdmin):
#    list_display = ('attribute_one', 'attribute_two', 'comparator')

class ModelTemplateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name', 'fields', 'is_group', 'drawing',)
    ordering = ('pk',)

class RelationTemplateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name', 'from_fields', 'to_fields', 'comparators',)
    ordering = ('pk',)



admin.site.register(Graph, GraphAdmin)
admin.site.register(GraphData, GraphDataAdmin)
admin.site.register(GraphModel, GraphModelAdmin)
admin.site.register(GraphRelation, GraphRelationAdmin)
admin.site.register(GraphModelDrawing, GraphModelDrawingAdmin)
admin.site.register(GraphNode, GraphNodeAdmin)
admin.site.register(ModelTemplate, ModelTemplateAdmin)
admin.site.register(RelationTemplate, RelationTemplateAdmin)

# admin.site.register(GraphAttributeComparator, GraphAttributeComparatorAdmin)
