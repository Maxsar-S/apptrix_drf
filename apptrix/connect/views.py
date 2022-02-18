import environ
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from connect.serializers import UserRegistrySerializer, UserSerializer, UserMatchSerializer
from connect.models import User
import smtplib


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrySerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class UserMatch(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        data = request.data.dict()
        data['user_like'] = request.user.username
        print(data)
        serializer = UserMatchSerializer(data=data)
        if serializer.is_valid():
            serializer.like()
            if serializer.like() == 'Match':
                username = data['username']
                mail = data['email']
                message_1 = f'Вы понравились {username}! Почта участника: {mail}'
                message_2 = f'Вы понравились {request.user.username}! Почта участника: {request.user.email}'
                send_letter(mail, request.user.email, message_1, message_2)
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


def send_letter(email1, email2, message1, message2):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()

    env = environ.Env()
    environ.Env.read_env()
    login_email = env('LOGIN_EMAIL')
    email_password = env('EMAIL_PASSWORD')
    smtpObj.login(login_email, email_password)

    smtpObj.sendmail(login_email, email1, message1)
    smtpObj.sendmail(login_email, email2, message2)
