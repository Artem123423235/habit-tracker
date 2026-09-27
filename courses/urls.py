from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')
router.register('lessons', LessonViewSet, basename='lessons')
router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
]
