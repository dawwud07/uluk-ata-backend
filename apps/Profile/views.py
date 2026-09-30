from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.Restaraunt.models import Cart

from .models import Address, Notification, Order, OrderItem
from .serializers import AddressSerializer, NotificationSerializer, OrderSerializer


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return Response(AddressSerializer(addresses, many=True).data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
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
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(AddressSerializer(address).data)

    def patch(self, request, pk):
        address = self.get_address(request, pk)
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_address(request, pk)
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
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
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializer(order).data)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = list(cart.items.select_related('dish'))
        if not cart_items:
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        fulfillment = request.data.get('fulfillment', 'delivery')
        if fulfillment not in ['delivery', 'pickup']:
            return Response({'fulfillment': 'Choose delivery or pickup.'}, status=status.HTTP_400_BAD_REQUEST)

        address = None
        address_text = ''
        if fulfillment == 'delivery':
            address = Address.objects.filter(
                user=request.user,
                id=request.data.get('address_id'),
            ).first()
            if not address:
                return Response({'address_id': 'Provide a delivery address.'}, status=status.HTTP_400_BAD_REQUEST)
            address_text = address.address

        phone = request.data.get('phone') or str(request.user.phone or '')
        if not phone:
            return Response({'phone': 'Provide a phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        subtotal = Decimal('0')
        for item in cart_items:
            subtotal += item.dish.price * item.quantity

        delivery_fee = Decimal('100') if fulfillment == 'delivery' else Decimal('0')
        order = Order.objects.create(
            user=request.user,
            fulfillment=fulfillment,
            address=address,
            address_snapshot=address_text,
            phone=phone,
            comment=request.data.get('comment', ''),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=subtotal + delivery_fee,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                name=item.dish.name,
                price=item.dish.price,
                quantity=item.quantity,
            )

        cart.items.all().delete()
        Notification.objects.create(
            user=request.user,
            order=order,
            
            title='Order accepted',
            message=f'Order #{order.id} is being prepared.',
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        return Response(NotificationSerializer(notifications, many=True).data)


class ReadNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'marked_read': count})
