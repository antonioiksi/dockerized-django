from rest_framework import serializers

from .models import Attribute, EntityAttribute, MappingType


class MappingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingType
        fields = '__all__'  # ('title', 'description', 'active')


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('name', )

#
# class AttributeNameSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Attribute
#        fields = ('name',)
###

class EntityAttributeSerializer(serializers.ModelSerializer):
    # attributes = AttributeNameSerializer(many=True, read_only=True)

    class Meta:
        model = EntityAttribute
        fields = ('name', 'title', )




class EntityAttributeSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntityAttribute
        fields = ('name', 'title',)
