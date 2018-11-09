from django.urls import path
from . import views, new_views

app_name = 'sop'
urlpatterns = [
    path('', views.home, name='home'),
    path('zc/', views.zc, name='zc'),
    path('<code>/succeed/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<code>/lo/', views.lo, name='lo'),
    path('update_password/', views.update_password, name='update_password'),
    path('passwords', views.passwords, name='passwords'),
    path('user_xx/', views.user_xx, name='user_xx'),
    path('log/', views.log, name='log'),
    path('yue/', views.yue, name='yue'),
    path('toup/', views.toup, name='toup'),
    path('manage/', views.manage, name='manage'),
    path('add_goods/', views.add_goods, name='add_goods'),
    path('add_goods_add/', views.add_goods_add, name='add_goods_add'),
    path('ll/', views.ll, name='ll'),
    path('goods_z/', views.goods_z, name='goods_z'),
    path('goods_id/', views.goods_id, name='goods_id'),
    path('update_goods/', views.update_goods, name='update_goods'),
    path('update_goo/', views.update_goo, name='update_goo'),
    path('update/', views.update, name='update'),
    path('all_goods/', views.all_goods, name='all_goods'),
    path('<page>/goods_cl/', views.goods_cl, name='goods_cl'),
    path('all_update/', views.all_update, name='all_update'),
    path('<goods_id>/state/', views.state, name='state'),
    path('<goods_id>/cancel/', views.cancel, name='cancel'),
    path('shop/', views.shop, name='shop'),
    path('<pages>/shops/', views.shops, name='shops'),
    path('deal/', views.deal, name='deal'),
    path('goods_record', views.goods_record, name='goods_record'),
    path('<pages>/cart/', views.cart, name='cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('close/', views.close, name='close'),
    path('<goods_id>/del_goods/', views.del_goods, name='del_goods'),
    path('del_all/', views.del_all, name='del_all'),
    path('<pages>/page/', views.page, name='page'),
    path('<pages>/next/', views.next, name='next'),
    path('show_login/', views.show_login, name='show_login'),
    path('homes/', views.homes, name='homes'),
    path('<pages>/record_pages/', views.record_pages, name='record_pages'),
    path('<pages>/record_next/', views.record_next, name='record_next'),
    path('upload/', views.upload, name='upload'),



]

urlpatterns +=[
    path('show_order/', new_views.show_order, name='show_order'),
    path('<goods_id>/<goods_stock>/order/', new_views.receive, name='receive'),
    path('admin/', new_views.admins, name='admin'),
    path('incomes/', new_views.incomes, name='incomes'),
    path('expend/', new_views.expend, name='expend'),
    path('<goods_id>/<goods_stock>/show_order/', new_views.returus, name='returns'),
    path('<page>/up_ll/', views.up_ll, name='up_ll'),
    path('<page>/down_ll/', views.down_ll, name='down_ll'),
    path('admin_time/', new_views.admin_time, name='admin_time'),
    path('times/', new_views.times, name='times'),
    path('index/', new_views.index, name='index')
]