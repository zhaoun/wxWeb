from rest_framework import serializers
from repairApi.models import RepairOrder, RepairFeedback
from django.contrib.auth.models import User


class RepairSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    worker = serializers.ReadOnlyField(source='worker.username')

    class Meta:
        model = RepairOrder
        fields = ('id', 'dorm', 'cause', 'owner', 'state', 'createTime', 'worker', 'image')


class RepairNotFeedbackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    worker = serializers.ReadOnlyField(source='worker.username')

    class Meta:
        model = RepairOrder
        fields = ('id', 'dorm', 'owner', 'worker')


class RepairFeedbackSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='order.owner.username')
    # owner = serializers.ReadOnlyField(source='owner.username')
    # owner = serializers.ReadOnlyField

    class Meta:
        model = RepairFeedback
        fields = ('id', 'order', 'feedback', 'update_time', )


class UserSerializer(serializers.ModelSerializer):
    repair_orders = serializers.PrimaryKeyRelatedField(many=True, queryset=RepairOrder.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'repair_orders', 'is_superuser', 'is_staff']


class AUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_superuser', 'is_staff']