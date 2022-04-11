from django.shortcuts import render
from rest_framework.views import APIView
from reportingapp.serializers import UserCreateSerializer,Loginserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class UserCreateMixin(generics.GenericAPIView,mixins.CreateModelMixin):

    model = User
    serializer_class = UserCreateSerializer

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class SigninView(APIView):

    serializer_class= Loginserializer

    def post(self,request):
        serializer = self.serializer_class(data =request.data)
        if serializer.is_valid():
            username = serializer.validated_data["user"]
            password= serializer.validated_data["password"]
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return Response({'msg':'login successfull'},status = status.HTTP_200_OK)
            else:
                return Response({'msg':"invalid user"},status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors)