from rest_framework import viewsets
from .models import Producer
from .serializers import ProducerSerializer


class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
