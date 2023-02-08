from rest_framework.generics import CreateAPIView

from core.serializers import CreateUserSerializer


class SignupView(CreateAPIView):
    serializer_class = CreateUserSerializer
