from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Log


class LogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)


class LogSearchSerializer(serializers.ModelSerializer):
    query = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    # user = LogUserSerializer()

    class Meta:
        model = Log
        fields = ('user', 'username', 'ip', 'datetime', 'query',)

    def get_query(self, obj):
        jsonQuery = None
        if obj.query is not None and type(obj.query) is dict:
            if 'jsonQuery' in obj.query.keys():
                jsonQuery = obj.query['jsonQuery']

        return jsonQuery

    def get_username(self, obj):
        if obj.user is None:
            return ''
        else:
            return obj.user.username

class LogSerializer(serializers.ModelSerializer):
    query = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = ('user', 'ip', 'datetime', 'query', 'event', 'method')

    def get_query(self, obj):
        attr_name = obj.query['query']['bool']['should'][0]['query_string']['default_field']
        attr_val = obj.query['query']['bool']['should'][0]['query_string']['query']
        return attr_name + ':' + attr_val





class LogSimpleSerializer(serializers.Serializer):
    ip = serializers.CharField(required=True, allow_blank=False, max_length=100)
    event = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Log` instance, given the validated data.
        """
        return Log.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Log` instance, given the validated data.
        """
        instance.ip = validated_data.get('ip', instance.ip)
        instance.event = validated_data.get('event', instance.event)
        instance.save()
        return instance
