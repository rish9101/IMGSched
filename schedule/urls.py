from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import home, MeetingViewSet


router = DefaultRouter()
router.register("meetings", MeetingViewSet)

urlpatterns = [
        path('', include(router.urls)),
    ]
