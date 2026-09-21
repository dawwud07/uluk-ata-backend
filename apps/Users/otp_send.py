import random 
from rest_framework.views import APIView
from .serializer import SendOTPSerializer , VerifyOTPSerializer , ResetPasswordSerilizer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import User , OTPCode
from django.utils import timezone 
from datetime import timedelta


code_storage = {}

class SendOTPCodeView(APIView):
    def post(self , request):
        serializer = SendOTPSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        email = serializer.validated_data['email']
        
        code = str(random.randint(100000 , 999999))
        
        otp = OTPCode.objects.create(
            email= email,
            code = code,
            expire_at= timezone.now() + timedelta(minutes=5),
            purpose='verification',
        )
        
        try:
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except (OSError, TimeoutError):
            otp.delete()
            return Response(
                {'error': 'Не удалось подключиться к почтовому серверу. Попробуйте позже.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
        
        return Response({'message': 'Код отправлен'})
    



class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        otp = OTPCode.objects.filter(email=email, code=code).first()

        if otp is None:
            return Response({'error': 'Сначала запросите код'}, status=status.HTTP_401_UNAUTHORIZED)

        if otp.is_expired():
            otp.delete()
            return Response({'error': 'Код истек, попросите новый'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Код подтвержден'}, status=status.HTTP_200_OK)



    
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        otp = OTPCode.objects.filter(email = email , code = code).first()
        
        if otp is None:
            return Response({'error': 'Сначала запросите код'} , status=status.HTTP_401_UNAUTHORIZED)
        
        if otp.is_expired():
            otp.delete()
            return Response({'error' : 'kod istek poprosi noviy'} , status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response({'error' : 'polzovatel ne nayden'} , status=status.HTTP_401_UNAUTHORIZED)
        
        user.set_password(new_password)
        user.save()

        otp.delete()
        

        return Response({'message': 'Пароль изменен'}, status=status.HTTP_200_OK)
    