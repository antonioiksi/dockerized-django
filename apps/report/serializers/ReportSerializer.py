from rest_framework import serializers

from apps.report.serializers.DataSerializer import DataSerializer


class ReportSerializer(serializers.Serializer):

    target = serializers.CharField(max_length=1000)
    results = DataSerializer(many=True)
