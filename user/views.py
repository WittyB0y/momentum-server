from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                key: value for key, value in serializer.validated_data.items() if key != 'password'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
