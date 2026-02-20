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

    type_display = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Producer
        fields = [
            "id",
            "name",
            "type",
            "type_display",  # original type + formatted display
            "description",
            "phone",
            "mobile_phone",
            "email",
            "website",
            "address",  # formatted address
            "facebook",
            "instagram",
            "twitter",
            "youtube",
            "tiktok",
            "main_image_url",
            "gallery_images",
            "products",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_main_image_url(self, obj):
        request = self.context.get("request")
        if obj.main_image and request:
            return request.build_absolute_uri(obj.main_image.url)
        return None

    def get_type_display(self, obj):
        """Return a string with the types separated by ' • '"""
        if isinstance(obj.type, list):
            return " • ".join(obj.type)
        return str(obj.type) if obj.type else ""

    def get_address(self, obj):
        """Return formatted address object"""
        parts = []
        if obj.street:
            street_addr = obj.street
            if obj.number:
                street_addr = f"{obj.number}, {obj.street}"
            parts.append(street_addr)
        if obj.city:
            parts.append(obj.city)
        if obj.zip_code:
            parts.append(obj.zip_code)

        return {
            "street": obj.street,
            "number": obj.number,
            "city": obj.city,
            "state": obj.state,
            "zip_code": obj.zip_code,
            "formatted": ", ".join(parts) if parts else "Morada não disponível",
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Move main_image_url to main_image
        data["main_image"] = data.pop("main_image_url", None)
        return data
