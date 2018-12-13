from rest_framework import serializers


class DataSerializer(serializers.Serializer):

    index_name = serializers.CharField(max_length=1000)
    data = serializers.ListField(serializers.DictField())
