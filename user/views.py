from user.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from user.serializers import PrinterSerializer, UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Custom handler for the JWT Response Payload. Default is just the JWT itself.
    This adds a serialized User to the response payload.
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }


def create_jwt(user):
    """
    Function to create a new JWT manually
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class Register(APIView):
    """
    View for Registering new Users
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Defines HTTP POST method for Register Endpoint
        """
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(serializer.initial_data['email'],
                                        serializer.initial_data['password'],
                                        first_name=serializer.initial_data['first_name'],
                                        last_name=serializer.initial_data['last_name'],
                                        is_vendor=serializer.initial_data['is_vendor'])

        token = create_jwt(user)

        return Response({
            'token': token,
            'user': serializer.data,
        }, status=status.HTTP_201_CREATED)


class PrinterList(APIView):
    """
    View for Registering new Printers
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Defines HTTP POST method for Register Endpoint
        """
        request.data['vendor'] = request.user.id
        serializer = PrinterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
