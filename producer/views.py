from rest_framework import viewsets
from .models import Producer
from .serializers import ProducerSerializer
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by type/category
        producer_type = self.request.query_params.get("type")
        if producer_type:
            queryset = queryset.filter(type__icontains=producer_type)

        # Filter by city
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset

    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
