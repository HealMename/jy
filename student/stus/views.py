from django.shortcuts import render,HttpResponseRedirect,reverse
from django.http import HttpResponse
from .models import Home,Student
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'stus/index_1.html'
    context_object_name = 'home_list'

    def get_queryset(self):
        return Home.objects.all()


def student(request, id):

    if id == 1:
        a = Student(stu_name=request.POST['name'], stu_age=request.POST['age'], stu_password=request.POST['password'])
        a.save()
        return render(request, 'stus/index_1.html')
    elif id == 2:
        pass


def zc(request):

    student_list = Home.objects.all()

    context = {'student_list': student_list}

    return render(request, 'stus/index_2.html', context)


def question(request, year):
    return HttpResponse(year)








# Create your views here.
