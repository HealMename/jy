from django.urls import path
from . import views
app_name = 'sop'
urlpatterns = [
    path('', views.home, name='home'),
    path('zc/', views.zc, name='zc'),
    path('<code>/succeed/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<code>/lo/', views.lo, name='lo'),
    path('<user_id>/update_password/', views.update_password, name='update_password'),
    path('<user_id>/passwords', views.passwords, name='passwords'),
    path('<user_id>/user_xx/', views.user_xx, name='user_xx'),
    path('<user_id>/log/', views.log, name='log'),
    path('<user_id>/yue/', views.yue, name='yue'),
    path('<user_id>/toup/', views.toup, name='toup'),
    path('<user_id>/manage/', views.manage, name='manage'),
    path('<user_id>/add_goods/', views.add_goods, name='add_goods'),
    path('<user_id>/add_goods_add/', views.add_goods_add, name='add_goods_add'),
    path('<user_id>/ll/', views.ll, name='ll'),
    path('<user_id>/goods_z/', views.goods_z, name='goods_z'),
    path('<user_id>/goods_id', views.goods_id, name='goods_id'),
    path('<user_id>/update_goods/', views.update_goods, name='update_goods'),
    path('<user_id>/update_goo/', views.update_goo, name='update_goo'),
    path('<user_id>/update/', views.update, name='update'),
    path('all_goods/', views.all_goods, name='all_goods'),
    path('<page>/goods_cl/', views.goods_cl, name='goods_cl'),
    path('<user_id>/all_update/', views.all_update, name='all_update'),
    path('<user_id>/<goods_id>/state/', views.state, name='state'),
    path('<user_id>/<goods_id>/cancel/', views.cancel, name='cancel'),
    path('<user_id>/shop/', views.shop, name='shop'),
    path('<user_id>/<pages>/shops/', views.shops, name='shops'),
    path('<user_id>/deal/', views.deal, name='deal'),
    path('<user_id>/get_goods/', views.get_goods, name='get_goods'),
    path('<user_id>/gets_goods/', views.gets_goods, name='gets_goods'),
    path('<user_id>/goods_record', views.goods_record, name='goods_record'),
    path('<user_id>/<pages>/cart/', views.cart, name='cart'),
    path('<user_id>/show_cart/', views.show_cart, name='show_cart'),
    path('<user_id>/close/', views.close, name='close'),
    path('<user_id>/<goods_id>/del_goods/', views.del_goods, name='del_goods'),
    path('<user_id>/del_all/', views.del_all, name='del_all'),
    path('<user_id>/<pages>/page/', views.page, name='page'),
    path('<user_id>/<pages>/next/', views.next, name='next'),
    path('<user_id>/show_login/', views.show_login, name='show_login'),
    path('<user_id>/homes/', views.homes, name='homes'),
    path('<user_id>/<pages>/record_pages/', views.record_pages, name='record_pages'),
    path('<user_id>/<pages>/record_next/', views.record_next, name='record_next'),



]