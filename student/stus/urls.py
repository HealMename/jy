from django.urls import path, register_converter
from . import views, url_converters

register_converter(url_converters.Four, 'xxx')

app_name = 'stus'
urlpatterns = [
 path('', views.IndexView.as_view(), name='index'),
 path('<int:id>', views.student, name='student'),
 path('zc/', views.zc, name='zc'),
 path('<xxx:year>/question/', views.question, name='question')
]