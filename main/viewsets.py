from rest_framework import viewsets

from . import models
from . import serializers


class recordsViewset(viewsets.ModelViewSet):
    queryset = models.Records.objects.all()
    serializer_class = serializers.RecordsSerializer