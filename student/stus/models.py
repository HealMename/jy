from django.db import models


class StuManager(models.Manager):

    def create_stu(self, stu_name, stu_age, stu_password):
        stu = self.create(stu_name=stu_name, stu_age=stu_age, stu_password=stu_password)
        stu.stu_name = '《'+stu_name+'》'
        Home.objects.create(vi_1=stu_name)
        stu.save()


class Student(models.Model):
    stu_name = models.CharField(max_length=10)
    stu_age = models.CharField(max_length=10)
    stu_password = models.CharField(max_length=10)
    stu_times = models.DateTimeField
    objects = StuManager()


class Home(models.Model):
    vi_1 = models.CharField(max_length=10)



