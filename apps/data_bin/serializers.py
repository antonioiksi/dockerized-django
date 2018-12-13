import json

from rest_framework import serializers

from .models import Bin, BinItem


class BinSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ('id', 'name')


class BinSerializer(serializers.ModelSerializer):
    data_row_count = serializers.SerializerMethodField()
    items_count = serializers.IntegerField(
        source='binitem_set.count',
        read_only=True
    )

    class Meta:
        model = Bin
        fields = ('id', 'user', 'name', 'active', 'items_count', 'data_row_count')

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if len(data['name']) < 2:
            raise serializers.ValidationError("'name' must contain more than 2 symbols")
        return data

    def get_data_row_count(self, obj):
        bin = obj
        count = 0
        for item in BinItem.objects.filter(bin=bin):
            count += len(item.data)
        return count


class BinItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinItem
        fields = ('id', 'bin', 'url', 'query', 'data', 'mapping',)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if len(data['data']) < 2:
            raise serializers.ValidationError("'data' must contain more than 2 symbols")
        return data


class BinItemSimpleSerializer(serializers.ModelSerializer):
    doc_count = serializers.SerializerMethodField()
    jsonQuery = serializers.SerializerMethodField()
    # bin = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # bin = serializers.StringRelatedField(read_only=True)
    bin = BinSimpleSerializer(read_only=True)

    class Meta:
        model = BinItem
        fields = ('id', 'datetime', 'bin', 'jsonQuery', 'doc_count',)

    def get_doc_count(self, obj):
        json_data = obj.data
        doc_count = len(json_data)
        return doc_count

    def get_jsonQuery(self, obj):
        if obj.query is not None:
            query = obj.query
            if 'jsonQuery' in query.keys():
                return query['jsonQuery']
            else:
                return query
        else:
            return None
