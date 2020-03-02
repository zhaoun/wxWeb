from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class RepairOrder(models.Model):
    STATE_WAIT = 1
    STATE_REPAIR = 2
    STATE_FINISH = 3
    STATE_ITEMS = (
        (STATE_WAIT, '等审批'),
        (STATE_REPAIR, '维修中'),
        (STATE_FINISH, '已完成'),
    )

    dorm = models.CharField(max_length=50, verbose_name='宿舍号')
    cause = models.CharField(max_length=200, verbose_name='故障问题')
    state = models.PositiveIntegerField(default=STATE_WAIT, choices=STATE_ITEMS, verbose_name='状态')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="报修时间")
    owner = models.ForeignKey('auth.User', related_name='repair_orders', on_delete=models.CASCADE)
    worker = models.ForeignKey('auth.User', related_name='repair_worker', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='img/', verbose_name='图片', null=True, blank=True)

    class Meta:
        # db_table = "WxRepair"
        verbose_name = verbose_name_plural = '微信维修'
        ordering = ['createTime']

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class RepairFeedback(models.Model):
    order = models.OneToOneField(RepairOrder, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=50, verbose_name='反馈评价')
    update_time = models.DateTimeField(auto_now=True, verbose_name='评价时间')

    class Meta:
        verbose_name = verbose_name_plural = '微信维修评价'
