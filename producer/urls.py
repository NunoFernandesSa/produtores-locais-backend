from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r"producers", views.ProducerViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
