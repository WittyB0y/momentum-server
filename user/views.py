from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, CheckIsAvailableUsernameSerializer


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


class CheckIsAvailableUsername(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CheckIsAvailableUsernameSerializer
    permission_classes = (AllowAny,)
    status_code = {
        True: status.HTTP_200_OK,
        False: status.HTTP_404_NOT_FOUND,
    }

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        result = self.queryset.filter(username=username).exists()

        return Response({'IsExist': result}, status=self.status_code[result])
