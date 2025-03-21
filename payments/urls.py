from django.urls import path, include

from .views import (
    InitiatePaymentView, PaymentSuccessView, PaymentFailView, PaymentCancelView, 
    AllPaymentsView, PaymentDetailView, UserPaymentsView
)


urlpatterns = [
    path("initiate/<int:order_id>/", InitiatePaymentView.as_view(), name="initiate_payment"),

    path("success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("fail/", PaymentFailView.as_view(), name="payment_fail"),
    path("cancel/", PaymentCancelView.as_view(), name="payment_cancel"),

    path("all/", AllPaymentsView.as_view(), name="payment_list"),
    path('user/<int:user_id>/', UserPaymentsView.as_view(), name='user-payments'),
    path("all/<int:pk>/", PaymentDetailView.as_view(), name="payment_detail"),
]
