from repairApi.models import RepairOrder, RepairFeedback
from repairApi.serializers import RepairSerializer, UserSerializer, AUserSerializer, RepairFeedbackSerializer, RepairNotFeedbackSerializer
from rest_framework import generics, permissions, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q
# from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


@api_view(['POST'])
def UserCreated(request):
    username = request.data['username']
    user_pass = request.data['password']
    user = User.objects.create_user(username=username, password=user_pass)
    return Response('success')


class RepairList(generics.ListCreateAPIView):
    # queryset = RepairOrder.objects.all()
    serializer_class = RepairSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        staff = self.request.user.is_staff
        if staff:
            return RepairOrder.objects.filter(Q(worker__isnull=True) | Q(worker=user))
        else:
            return RepairOrder.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RepairDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(worker=self.request.user)


class RepairFeedbackList(generics.ListCreateAPIView):
    queryset = RepairFeedback.objects.all()
    serializer_class = RepairFeedbackSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class RepairFeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairFeedback.objects.all()
    serializer_class = RepairFeedbackSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class RepairNotFeedBackList(generics.ListCreateAPIView):
    serializer_class = RepairNotFeedbackSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        staff = self.request.user.is_staff
        feedback_id = RepairFeedback.objects.values_list('order')
        if staff:
            return RepairOrder.objects.filter(worker=user, state=3).exclude(id__in=feedback_id)
        else:
            return RepairOrder.objects.filter(owner=user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]


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


class AUser(generics.RetrieveAPIView):
    serializer_class = AUserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        return self.request.user
