from django.db import models
from django.utils import timezone


# class GoodsManager(models.Manager):
#
#     def update_goods(self, goods_name, goods_id, goods_price, goods_class, goods_stock, goods_update, goods_user):
#         self.update(goods_name=goods_name,
#                     goods_id=goods_id,
#                     goods_price=goods_price,
#                     goods_class=goods_class,
#                     goods_stock=goods_stock,
#                     goods_user=goods_user,
#                     goods_update=goods_update)
#         Update.objects.create(goods_id=goods_id,
#                               goods_text='我修改了'+goods_name+'商品',
#                               goods_user=goods_user)
#
#     def create_goods(self,goods_name, goods_id, goods_price, goods_class, goods_stock, goods_update, goods_user):
#         self.create(goods_name=goods_name,
#                     goods_id=goods_id,
#                     goods_price=goods_price,
#                     goods_class=goods_class,
#                     goods_stock=goods_stock,
#                     goods_user=goods_user,
#                     goods_update=goods_update)
class User_bill(models.Model):
    water = models.CharField(max_length=2)
    times = models.DateTimeField(default=timezone.now)


class Users(models.Model):
    user_name = models.CharField(max_length=10)
    user_account = models.CharField(max_length=6)
    user_password = models.CharField(max_length=200)
    user_question = models.CharField(max_length=50)
    user_answer = models.CharField(max_length=50)
    user_RMB = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    user_time = models.DateTimeField(default=timezone.now)
    user_home = models.CharField(max_length=40, default='')
    user_income = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    user_expend = models.DecimalField(max_digits=60, decimal_places=2, default=0)


class Goods(models.Model):
    goods_name = models.CharField(max_length=20)
    goods_id = models.CharField(max_length=21, primary_key=True)
    goods_price = models.DecimalField(decimal_places=2, max_digits=60)
    goods_class = models.CharField(max_length=10)
    goods_stock = models.IntegerField(default=99)
    goods_time = models.DateTimeField(default=timezone.now)
    goods_update = models.DateField('修改时间')
    goods_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    goods_state = models.CharField(max_length=3, default='未上架')
    goods_delete = models.CharField(max_length=3, default='0')
    goods_address = models.CharField(max_length=40, default='北京')


class Update(models.Model):
    goods_id = models.CharField(max_length=21)
    goods_update = models.DateTimeField(default=timezone.now)
    goods_text = models.CharField(max_length=200)
    goods_user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Cart(models.Model):
    goods_name = models.CharField(max_length=20)
    goods_price = models.DecimalField(decimal_places=2, max_digits=60)
    goods_x = models.IntegerField()
    goods_id = models.CharField(max_length=21)
    goods_user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Logins(models.Model):
    login_time = models.DateTimeField(default=timezone.now)
    logout = models.CharField(max_length=2, default='登录')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Deal_goods(models.Model):
    goods_name = models.CharField(max_length=20)
    goods_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    goods_id = models.CharField(max_length=21)
    goods_price = models.DecimalField(decimal_places=2, max_digits=60)
    goods_stock = models.IntegerField()
    goods_time = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    order_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    goods_name = models.CharField(max_length=20)
    goods_id = models.CharField(max_length=21)
    goods_stock = models.CharField(max_length=99)
    goods_address = models.CharField(max_length=40)
    user_home = models.CharField(max_length=40)
    address_time = models.DateTimeField(default=timezone.now)
    yes_goods = models.CharField(max_length=10, default='未收货')


class Admins(models.Model):
    water = models.CharField(max_length=2)
    detail = models.CharField(max_length=62, default='')
    times = models.DateTimeField(default=timezone.now)

