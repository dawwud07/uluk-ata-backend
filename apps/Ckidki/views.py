from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Promotion
from .serializer import PromotionListSerializer, PromotionDetailSerializer


class PromotionListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        promotions = Promotion.objects.filter(is_active=True)
        serializer = PromotionListSerializer(promotions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PromotionDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        promotion = get_object_or_404(Promotion, pk=pk, is_active=True)
        serializer = PromotionDetailSerializer(promotion)
        return Response(serializer.data, status=status.HTTP_200_OK)