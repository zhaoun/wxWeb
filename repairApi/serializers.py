from rest_framework import serializers
from repairApi.models import RepairOrder
from django.contrib.auth.models import User


class RepairSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = RepairOrder
        fields = ('id', 'dorm', 'cause', 'owner', 'state', 'createTime')


class UserSerializer(serializers.ModelSerializer):
    repair_orders = serializers.PrimaryKeyRelatedField(many=True, queryset=RepairOrder.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'repair_orders']


# class RepairNumSerializer(serializers.ModelSerializer):
#     start = serializers.ReadOnlyField(RepairOrder.objects.filter(state='1', owner=user).count())
#     wait = serializers.ReadOnlyField()
#     end = serializers.ReadOnlyField()