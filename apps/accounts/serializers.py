from rest_framework import serializers

from .models import Role, User


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role

        fields = (
            "id",
            "name",
            "description",
        )


class UserSerializer(serializers.ModelSerializer):

    role = RoleSerializer(
        read_only=True
    )

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "date_joined",
        )

        read_only_fields = (
            "id",
            "date_joined",
            "role",
        )