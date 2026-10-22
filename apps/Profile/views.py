from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsSuperUser

from .models import Address, Notification, Order
from .serializers import (
    AddressSerializer,
    NotificationSerializer,
    OrderReviewSerializer,
    OrderSerializer,
)
from .services import create_order_from_cart, set_order_status


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return Response(AddressSerializer(addresses, many=True).data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                Address.objects.filter(user=request.user).update(is_default=False)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_address(self, request, pk):
        return Address.objects.filter(user=request.user, id=pk).first()

    def get(self, request, pk):
        address = self.get_address(request, pk)
        if not address:
            return Response(
                {"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(AddressSerializer(address).data)

    def patch(self, request, pk):
        address = self.get_address(request, pk)
        if not address:
            return Response(
                {"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                Address.objects.filter(user=request.user).exclude(id=address.id).update(
                    is_default=False
                )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        address = self.get_address(request, pk)
        if not address:
            return Response(
                {"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                Address.objects.filter(user=request.user).exclude(id=address.id).update(
                    is_default=False
                )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_address(request, pk)
        if not address:
            return Response(
                {"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND
            )
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = Order.objects.filter(user=request.user, id=pk).first()
        if not order:
            return Response(
                {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(OrderSerializer(order).data)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order, error = create_order_from_cart(request.user, request.data)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        return Response(NotificationSerializer(notifications, many=True).data)


class ReadNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True
        )
        return Response({"marked_read": count})


class UpdateOrderStatusView(APIView):
    permission_classes = [IsSuperUser]

    def patch(self, request, pk):
        order = Order.objects.filter(id=pk).first()
        if not order:
            return Response(
                {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
        new_status = request.data.get("status")
        try:
            order = set_order_status(order, new_status)
        except ValueError:
            return Response(
                {"status": "Unknown status."}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(OrderSerializer(order).data)


class OrderReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = Order.objects.filter(user=request.user, id=pk).first()
        if not order:
            return Response(
                {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if hasattr(order, "review"):
            return Response(
                {"detail": "Order already reviewed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = OrderReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            user=request.user, status="delivered", review__isnull=True
        )
        return Response(OrderSerializer(orders, many=True).data)
