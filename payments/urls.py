from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, CreateCheckoutSessionView, PaymentListView

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('payment-list/', PaymentListView.as_view(), name='payment-list'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]
