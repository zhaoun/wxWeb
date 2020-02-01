from repairApi.models import RepairOrder
from repairApi.serializers import RepairSerializer, UserSerializer
from rest_framework import generics, permissions, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


@api_view(['POST'])
def UserCreated(request):
    username = request.data['username']
    user_pass = request.data['password']
    user = User.objects.create_user(username=username, password=user_pass)
    return Response('success')


# @api_view(['POST'])
# def UserLogin(request):
#     username = request.data['username']
#     user_pass = request.data['password']
#     user = authenticate(username=username, password=user_pass)
#     if user is not None:
#         token = Token.objects.get_or_create(user=username)
#         return Response({'Token': token})


class RepairList(generics.ListCreateAPIView):
    # queryset = RepairOrder.objects.all()
    serializer_class = RepairSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return RepairOrder.objects.filter(owner=user)

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


class RepairNum(views.APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        start = RepairOrder.objects.filter(state='1', owner=user).count()
        wait = RepairOrder.objects.filter(state='2', owner=user).count()
        end = RepairOrder.objects.filter(state='3', owner=user).count()
        return Response(dict(num={
            'wait': start,
            'start': wait,
            'end': end
        }))

