from rest_framework.serializers import ModelSerializer
from todoapp.models import Todo
from django.contrib.auth.models import User
from rest_framework import serializers


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields =["username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data["username"], password=validated_data["password"],
                                            email=validated_data["email"])


class TodoSerializer(ModelSerializer):
    user = UserCreateSerializer()
    class Meta:
        model = Todo
        fields =["task_name","completed","user"]


class Loginserializer(serializers.Serializer):
    user = serializers.CharField()
    password = serializers.CharField()
