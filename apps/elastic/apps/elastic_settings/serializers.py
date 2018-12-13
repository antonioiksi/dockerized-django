from rest_framework import serializers

from .models import ElasticSettings


class ElasticSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElasticSettings
        fields = ('id', 'user', 'name', 'title', 'setting',)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        data = data.decode('utf-8')

        if " " in data['name']:
            raise serializers.ValidationError("fount space symbol in 'name' field, please remove any space from name")


        return data
