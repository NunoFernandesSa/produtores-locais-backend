from rest_framework import serializers
from .models import Producer, ProducerImage


class ProducerImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProducerImage
        fields = ["id", "image_url", "caption", "order"]
        read_only_fields = ["id", "uploaded_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProducerSerializer(serializers.ModelSerializer):
    gallery_images = ProducerImageSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Producer
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_main_image_url(self, obj):
        request = self.context.get("request")
        if obj.main_image and request:
            return request.build_absolute_uri(obj.main_image.url)
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["main_image"] = data.pop("main_image_url", None)
        return data
