from rest_framework import serializers
from user.models import Printer, User


class UserSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for User Model
    """

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'date_joined', 'password',
                   'last_login', 'is_superuser', 'groups', 'user_permissions')


class PrinterSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for Printer Model
    """

    class Meta:
        model = Printer
        fields = '__all__'
