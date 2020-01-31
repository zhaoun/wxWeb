from repairApi.models import RepairOrder
from repairApi.serializers import RepairSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication


@api_view(['GET'])
def GetNums(request):
    start = RepairOrder.objects.filter(state='1').count()
    wait = RepairOrder.objects.filter(state='2').count()
    end = RepairOrder.objects.filter(state='3').count()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    return Response(dict(num={
        'wait': start,
        'start': wait,
        'end': end
    }))


@api_view(['POST'])
def UserCreated(request):
    username = request.data['username']
    user_pass = request.data['password']
    user = User.objects.create_user(username=username, password=user_pass)
    return Response('success')


@api_view(['POST'])
def UserLogin(request):
    username = request.data['username']
    user_pass = request.data['password']
    user = authenticate(username=username, password=user_pass)
    if user is not None:
        token = Token.objects.get_or_create(user=username)
        return Response({'Token': token})


class RepairList(generics.ListCreateAPIView):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RepairDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]