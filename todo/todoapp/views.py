from django.shortcuts import render
from rest_framework.views import APIView
from todoapp.models import Todo
from todoapp.serializers import TodoSerializer,UserCreateSerializer,Loginserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.
class TodoList(APIView):

    model = Todo
    serializer_class = TodoSerializer

    def get(self,request):
        todos = self.model.objects.all()
        serializer = self.serializer_class(todos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TodoDetails(APIView):
    model = Todo
    serializer_class= TodoSerializer

    def get_object(self,id):
        return self.model.objects.get(id=id)

    def get(self,request,*args,**kwargs):
        todo = self.get_object(kwargs["id"])
        serializer = self.serializer_class(todo)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        todo = self.get_object(kwargs["id"])
        serializer = self.serializer_class(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        todo = self.get_object(kwargs["id"])
        todo.delete()
        return Response(status = status.HTTP_200_OK)

class TodoMixinList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    model = Todo
    serializer_class = TodoSerializer
    queryset = model.objects.all()
    # authentication_classes = [BasicAuthentication,SessionAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class TodoMixinDetails(generics.GenericAPIView,mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    model = Todo
    serializer_class = TodoSerializer
    queryset = model.objects.all()
    lookup_field = "id"
    # authentication_classes = [BasicAuthentication,SessionAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def perform_update(self, serializer):
        user=self.request.user
        serializer.save(user=self.request.user)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


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
                token,created = Token.objects.get_or_create(user=user)
                return Response({'token':token.key},status = status.HTTP_200_OK)
            else:
                return Response({'msg':"invalid user"},status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors)