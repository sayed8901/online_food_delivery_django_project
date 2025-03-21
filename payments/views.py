from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status
from django.conf import settings
from django.urls import reverse

from sslcommerz_lib import SSLCOMMERZ
from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer


from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.permissions import IsOwnerOrReadOnly

from drf_spectacular.utils import extend_schema





# Creating class to initiate payment integration for a job post
class InitiatePaymentView(APIView):
    serializer_class = PaymentSerializer

    # Method initiate payment integration using SSLCommerz
    def initiate_ssl_payment(self, order):
        # SSLCommerz settings
        ssl_settings = {
            'store_id': settings.SSLCOMMERZ['store_id'],
            'store_pass': settings.SSLCOMMERZ['store_pass'],
            'issandbox': settings.SSLCOMMERZ['issandbox'],
        }

        # Create an SSLCommerz instance
        sslcz = SSLCOMMERZ(ssl_settings)

        # Transaction ID
        transaction_id = f"foodOrder_{order.id}"

        # Payment data
        post_body = {
            'total_amount': order.total_cost,
            'currency': "BDT",
            'tran_id': transaction_id,

            # Generate absolute URLs for redirection after payment:
            # - `reverse(...)` gets the relative path for each view.
            # - `build_absolute_uri(...)` converts the relative path to an absolute URL based on the request's host and protocol.
            'success_url': self.request.build_absolute_uri(reverse('payment_success')),
            'fail_url': self.request.build_absolute_uri(reverse('payment_fail')),
            'cancel_url': self.request.build_absolute_uri(reverse('payment_cancel')),

            'cus_name': self.request.user.username,
            'cus_email': self.request.user.email,
            'cus_phone': '01915158901',
            'cus_add1': 'Narayanganj',
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            
            'shipping_method': 'NO',
            'product_name': "Food Order",
            'num_of_item': 1,
            'product_category': "Food",
            'product_profile': 'general',
        }

        # Initiate payment session
        response = sslcz.createSession(post_body) # API response

        # # print to check the response
        # print("SSLCommerz Response:", response)

        return response



    # Payment POST request
    def post(self, request, order_id):
        if not order_id:
            return Response({"error": "Order ID is required"}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(pk = order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order info not found"}, status = status.HTTP_404_NOT_FOUND)


        # Ensure only unpaid order can be paid for
        if order.is_payment_done:
            return Response({"error": "Payment already completed for this order."}, status = status.HTTP_400_BAD_REQUEST)


        # Initiate the payment
        response = self.initiate_ssl_payment(order)

        if response.get('status') == 'SUCCESS':
            return Response({
                "message": "Payment initiated successfully",
                "gateway_url": response['GatewayPageURL'],
            })
        else:
            return Response({"error": "Failed to initiate payment"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)






# action to define for successful payment
class PaymentSuccessView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        # retrieving transaction_id and validation_id
        tran_id = request.data.get('tran_id')
        val_id = request.data.get('val_id')

        print('Transaction_id:', tran_id, 'Validation_id:', val_id)
        # print(request.data)


        if tran_id and val_id:
            order_id = int(tran_id.split('_')[1])
            # print('Order_id after payment success:', order_id)

            try:
                order = Order.objects.get(pk = order_id)

                # setting the payment completion to True
                order.is_payment_done = True
                
                order.save()



                # Save the payment information
                Payment.objects.create(
                    order = order,

                    tran_id = request.data.get('tran_id'),
                    val_id = request.data.get('val_id'),

                    amount = request.data.get('amount'),
                    currency = request.data.get('currency'),

                    card_type = request.data.get('card_type'),
                    card_brand = request.data.get('card_brand'),
                    bank_tran_id = request.data.get('bank_tran_id'),

                    store_id = request.data.get('store_id'),
                    verify_sign = request.data.get('verify_sign'),

                    tran_date = request.data.get('tran_date'),

                    status = "Completed"
                )


                # return Response({"message": "Payment completed successfully"})

                # TODO: check the frontend url
                redirect_url = f'http://localhost:5173/payment/success/{order_id}'
                # redirect_url = f'https://bd-job-portal.netlify.app/payment/success/{order_id}'
                print('url to redirect after payment success:', redirect_url)

                return HttpResponseRedirect(redirect_url)
            
            except Order.DoesNotExist:
                return Response({"error": "Job post not found"}, status = status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Payment validation failed"}, status = status.HTTP_400_BAD_REQUEST)




# for payment failures
class PaymentFailView(APIView):
    serializer_class = PaymentSerializer
    
    def post(self, request):
        # return Response({"message": "Payment failed, please try again."}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: check the frontend url
        redirect_url = f'http://localhost:5173/my_orders'
        # redirect_url = f'https://bd-job-portal.netlify.app/my_orders'
        print('url to redirect if payment fail:', redirect_url)

        return HttpResponseRedirect(redirect_url)




# for cancel payment
class PaymentCancelView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        # return Response({"message": "Payment canceled by user."}, status=status.HTTP_200_OK)

        # TODO: check the frontend url
        redirect_url = f'http://localhost:5173/my_orders'
        # redirect_url = f'https://bd-job-portal.netlify.app/my_orders'
        print('url to redirect if payment canceled:', redirect_url)

        return HttpResponseRedirect(redirect_url)






# payment list view set
class AllPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Payment.objects.all()


    @extend_schema(operation_id="list_all_payments")
    def get(self, request, *args, **kwargs):
        """Retrieve all payments."""
        return super().get(request, *args, **kwargs)





# Get all payments of a specific user
class UserPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Payment.objects.filter(order__user__id=user_id)
    




# payment detail view set
class PaymentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Payment.objects.all()


    @extend_schema(operation_id="retrieve_payment_by_id")
    def get(self, request, *args, **kwargs):
        """Retrieve payment details by ID."""
        return super().get(request, *args, **kwargs)


    @extend_schema(operation_id="delete_payment_by_id")
    def delete(self, request, *args, **kwargs):
        """Delete a payment record and mark the order as unpaid."""
        payment = self.get_object()
        
        # Update the associated order's payment status
        order = get_object_or_404(Order, id=payment.order.id)
        order.is_payment_done = False
        order.save()

        # Delete payment record
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


