from django.shortcuts import render
from .models import *
import time
import math
import random
from django.db.models import F
import hashlib


def home(request):
    return render(request, 'sop/home.html')


def homes(request, user_id):
    user = Users.objects.get(pk=user_id)
    Logins.objects.create(logout='退出', user=user)
    return render(request, 'sop/home.html')


def zc(request):
    code = str(random.randint(0, 9))+str(chr(random.randrange(65, 90))*3)
    return render(request, 'sop/register.html', {'code': code,
                                                 'nots': '欢迎注册'})


def register(request, code):
    user = Users.objects.filter(user_account=request.POST['account']).exists()
    if code == request.POST['code'] and not user:
        if 0 < len(request.POST['name']) < 20:
            if 30 > len(request.POST['question']) > 0:
                if 30 > len(request.POST['answer']) > 0:
                    if 30 > len(request.POST['account']) > 0:
                        md5 = hashlib.md5()
                        salt = '!!qwhrkjqhr'
                        md5.update(request.POST['passwords'].encode('utf8'))
                        md5.update(salt.encode('utf8'))
                        password = md5.hexdigest()
                        Users.objects.create(user_name=request.POST['name'],
                                             user_account=request.POST['account'],
                                             user_password=password,
                                             user_question=request.POST['question'],
                                             user_answer=request.POST['answer'])
                        return render(request, 'sop/register.html', {'code': code, 'nots': '注册成功'})
                else:
                    code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
                    return render(request, 'sop/register.html', {'code': code, 'nots': '请输入密保答案。用于重置密码'})
            else:
                code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
                return render(request, 'sop/register.html', {'code': code, 'nots': '请输入密保问题，用于充值密码'})
        else:
            code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
            return render(request, 'sop/register.html', {'code': code, 'nots': '昵称长度不能大于20或小于0'})
    else:
        code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
        return render(request, 'sop/register.html', {'code': code, 'nots': '验证码错误'})


def login(request):
    code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
    return render(request, 'sop/login.html', {'code': code})


def lo(request, code):
    if code == request.POST['code']:
        if len(request.POST['password']) > 0:
            md5 = hashlib.md5()
            salt = '!!qwhrkjqhr'
            md5.update(request.POST['password'].encode('utf8'))
            md5.update(salt.encode('utf8'))
            password = md5.hexdigest()
            if len(request.POST['account']) > 0:
                user = Users.objects.filter(user_account=request.POST['account']).filter(user_password=password).exists()

                if user:
                    users = Users.objects.get(user_account=request.POST['account'])
                    Logins.objects.create(user=users)
                    return render(request, 'sop/goods.html', {'users': users.id})
                else:
                    code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
                    return render(request, 'sop/login.html', {'code': code, 'not_account': '账号或密码不存在\n 请重试！'})
            else:
                code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
                return render(request, 'sop/login.html', {'code': code})
        else:
            code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
            return render(request, 'sop/login.html', {'code': code})
    else:
        code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
        return render(request, 'sop/login.html', {'code': code, 'not_code': '验证码错误！'})


def update_password(request, user_id):
    user = Users.objects.get(pk=user_id)
    return render(request, 'sop/update_password.html', {'user': user})


def passwords(request, user_id):
    user = Users.objects.get(pk=user_id)
    if user.user_answer == request.POST['answer']:
        user.user_password = request.POST['passwords']
        user.save()
        return render(request, 'sop/update_password.html', {'new': '修改成功', 'user': user})
    else:
        return render(request, 'sop/update_password.html', {'user': user, 'posswords': '密报问题错误'})


def user_xx(request, user_id):
    user = Users.objects.get(pk=user_id)
    return render(request, 'sop/user_xx.html', {'user_xx': user})


def log(request, user_id):
    return render(request, 'sop/goods.html', {'users': user_id})


def yue(request, user_id):
    return render(request, 'sop/yue.html', {'user_id': user_id})


def toup(request, user_id):
    Users.objects.filter(pk=user_id).update(user_RMB=request.POST['rmb']+F('user_RMB'))
    return render(request, 'sop/goods.html', {'users': user_id})


def manage(request, user_id):
    return render(request, 'sop/user_goods.html', {'user_id': user_id})


def add_goods(request, user_id):
    return render(request, 'sop/add_goods.html', {'user_id': user_id})


def add_goods_add(request, user_id):
    tim = math.ceil(time.time())
    try:
        user = Users.objects.get(id=user_id)
        goods = Goods.objects.create(goods_name=request.POST['name'],
                                     goods_id=request.POST['goods_class'] + str(tim) + str(random.randint(1, 10)) * 6,
                                     goods_price=request.POST['price'],
                                     goods_class=request.POST['goods_class'],
                                     goods_stock=request.POST['stock'],
                                     goods_user=user,
                                     goods_update=timezone.now())

        Update.objects.create(goods_id=goods.goods_id,
                              goods_text='添加了'+request.POST['name']+'商品',
                              goods_user=user)
    except:
        return render(request, 'sop/add_goods.html', {'user_id': user_id,
                                                      'cs': '请重试'})
    return render(request, 'sop/goods.html', {'users': user_id})


def ll(request, user_id):
    user = Users.objects.get(pk=user_id)
    user_goods = Goods.objects.filter(goods_user_id=user)
    return render(request, 'sop/user_goodsall.html', {'user_goods': user_goods,
                                                      'user': user})


def goods_z(request, user_id):
    return render(request, 'sop/goods_z.html', {'user_id': user_id})


def goods_id(request, user_id):
    try:
        goods = Goods.objects.exclude(goods_delete='1').get(goods_id=request.POST['goods_idd'])


    except:
        return render(request, 'sop/goods_z.html', {'user_id': user_id,
                                                    'goods_ex': '没有该商品'})

    if not goods:
        return render(request, 'sop/goods_z.html', {'user_id': user_id,
                                                    'goods_delete': '已删除'})
    else:
        return render(request, 'sop/goods_z.html', {'user_id': user_id,
                                                    'goods_id': goods})


def update_goods(request, user_id):
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.filter(goods_user_id=user_id)
    return render(request, 'sop/update_goods.html', {'goods': goods,
                                                     'user': user})


def update_goo(request, user_id):
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.get(pk=request.POST['update_goods'])
    return render(request, 'sop/update_goo.html', {'user': user,
                                                   'goods': goods
                                                   })


def update(request, user_id):
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.filter(pk=request.POST['goods_id'])
    if len(request.POST['name']) > 0 and int(request.POST['price']) > 0:
        goods.update(
            goods_name=request.POST['name'],
            goods_price=request.POST['price'],
            goods_class=request.POST['goods_class'],
            goods_update=timezone.now(),
        )
        Update.objects.create(goods_id=goods[0].goods_id,
                              goods_text='我修改了'+goods[0].goods_name+'的信息',
                              goods_user=user)

        return render(request, 'sop/update_goo.html', {'goodss': goods,
                                                       'user': user})

    else:
        return render(request, 'sop/update_goo.html', {'goods': goods,
                                                       'user': user,
                                                       'qcs': '请重试'})


def all_goods(request):
    page = 1
    goods = Goods.objects.exclude(goods_state='未上架')[(page-1)*4:page*4]
    return render(request, 'sop/all_goods.html', {'all_goods': goods,
                                                  'page': page})


def goods_cl(request, page):
    page = int(page)
    goods = Goods.objects.filter(goods_class=request.POST['goods_class'],
                                 goods_state='已上架')[(page-1)*4:page*4]
    if goods:
        return render(request, 'sop/all_goods.html', {'goods_class': goods,
                                                      'page': page})
    elif request.POST['goods_class'] == 'ALL':
        goods = Goods.objects.exclude(goods_state='未上架')[(page-1)*4:page*4]
        return render(request, 'sop/all_goods.html', {'all_goods': goods,
                                                      'page': page})


def all_update(request, user_id):
    user = Users.objects.get(id=user_id)
    goods_update = Update.objects.filter(goods_user=user)
    return render(request, 'sop/all_update.html', {'goods_update': goods_update,
                                                   'user': user})


def state(request, user_id, goods_id):
    Goods.objects.filter(goods_id=goods_id).update(goods_state='已上架')
    goods = Goods.objects.filter(goods_user_id=user_id)
    user = Users.objects.get(pk=user_id)
    return render(request, 'sop/user_goodsall.html', {'user': user,
                                                      'user_goods': goods})


def cancel(request, user_id, goods_id):
    Goods.objects.filter(goods_id=goods_id).update(goods_state='未上架')
    goods = Goods.objects.filter(goods_user_id=user_id)
    user = Users.objects.get(pk=user_id)
    return render(request, 'sop/user_goodsall.html', {'user': user,
                                                      'user_goods': goods})


def shops(request, user_id, pages):

    pages = int(pages)
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.get(goods_id=request.POST['goods_id'])
    all_goods = Goods.objects.filter(goods_state='已上架')[(pages-1)*4:pages*4]
    if request.POST['stock']:
        if int(goods.goods_stock) > int(request.POST['stock']):
            if user.user_RMB > goods.goods_price:
                Users.objects.filter(pk=user_id).update(user_RMB=user.user_RMB - goods.goods_price)
                Goods.objects.filter(pk=goods.goods_id).update(goods_stock=F('goods_stock') - request.POST['stock'])
                Deal_goods.objects.create(goods_name=goods.goods_name,
                                          goods_user=user,
                                          goods_id=goods.goods_id,
                                          goods_price=goods.goods_price,
                                          goods_stock=request.POST['stock'])
                return render(request, 'sop/shop.html', {'user': user,
                                                         'goods': all_goods,
                                                         'pages': pages,
                                                         'succeed': '成功购买！'})
            else:
                return render(request, 'sop/shop.html', {'user': user,
                                                         'goods': all_goods,
                                                         'pages': pages,
                                                         'succeed': '余额不足请充值！'})
        else:
            return render(request, 'sop/shop.html', {'user': user,
                                                     'goods': all_goods,
                                                     'pages': pages,
                                                     'succeed': '我们没有那么多库存了！'})
    else:
        return render(request, 'sop/shop.html', {'user': user,
                                                 'goods': all_goods,
                                                 'pages': pages,
                                                 'succeed': '请输入要购买的数量'})


def deal(request, user_id):
    user = Users.objects.get(pk=user_id)
    return render(request, 'sop/deal.html', {'user': user})


def get_goods(request, user_id):
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.filter(goods_state='已上架')
    return render(request, 'sop/get_goods.html', {'user': user,
                                                  'goods': goods})


def gets_goods(request, user_id):
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.filter(goods_state='已上架')
    if request.POST['goods_id']:
        goodss = Goods.objects.get(pk=request.POST['goods_id'])
        if request.POST['stock']:
            if int(goodss.goods_stock) > int(request.POST['stock']):
                if user.user_RMB > goodss.goods_price:
                    Users.objects.filter(pk=user_id).update(user_RMB=user.user_RMB - goodss.goods_price)
                    Goods.objects.filter(pk=goodss.goods_id).update(goods_stock=F('goods_stock') - request.POST['stock'])
                    Deal_goods.objects.create(goods_name=goodss.goods_name,
                                              goods_user=user,
                                              goods_id=goodss.goods_id,
                                              goods_price=goodss.goods_price,
                                              goods_stock=request.POST['stock'],
                                              )
                    return render(request, 'sop/get_goods.html', { 'user': user,
                                                                   'goods': goods,
                                                                   'succeed': '成功购买！'})
                else:
                    return render(request, 'sop/get_goods.html', {'user': user,
                                                                  'goods': goods,
                                                                  'succeed': '余额不足请充值！'})

            else:
                return render(request, 'sop/get_goods.html', {'user': user,
                                                              'goods': goods,
                                                              'succeed': '我们没有那么多库存了！'})
        else:
            return render(request, 'sop/get_goods.html', {'user': user,
                                                          'goods': goods,
                                                          'succeed': '请输入要购买的数量'})
    else:
        return render(request, 'sop/get_goods.html', {'user': user,
                                                      'goods': goods,
                                                      'succeed': '请输入商品编号'})


def goods_record(request, user_id):
    pages = 1
    user = Users.objects.get(pk=user_id)
    goodsr = Deal_goods.objects.filter(goods_user=user)
    goods = Deal_goods.objects.filter(goods_user=user)[0:4]
    if goodsr:
        a = 0
        print(goodsr)
        list_1 = []
        for i in goodsr:
            a = a + 1
            e = int(i.goods_price) * i.goods_stock
            list_1.append(e)
            if a == goodsr.count():
                return render(request, 'sop/goods_record.html', {'goods': goods,
                                                                 'user': user,
                                                                 'all_rmb': sum(list_1),
                                                                 'pages': pages,
                                                                 })

    else:
        return render(request, 'sop/goods_record.html', {'goods': goods, 'user': user, 'succeed': '您还没有购买过任何商品呢'})


def record_pages(request, user_id, pages):
    pages = int(pages)
    if pages == 1:
        user = Users.objects.get(pk=user_id)
        goods = Deal_goods.objects.filter(goods_user=user)[0:4]
        goodsr = Deal_goods.objects.filter(goods_user=user)
        a = 0
        list_1 = []
        for i in goodsr:
            a = a + 1
            e = int(i.goods_price) * i.goods_stock
            list_1.append(e)
            if a == goodsr.count():
                return render(request, 'sop/goods_record.html', {'goods': goods,
                                                                 'user': user,
                                                                 'all_rmb': sum(list_1),
                                                                 'pages': pages})
    else:
        pages = pages - 1
        user = Users.objects.get(pk=user_id)
        goods = Deal_goods.objects.filter(goods_user=user)[(pages-1)*4:pages*4]
        goodsr = Deal_goods.objects.filter(goods_user=user)
        if goodsr:
            a = 0
            list_1 = []
            for i in goodsr:
                a = a + 1
                e = int(i.goods_price) * i.goods_stock
                list_1.append(e)
                if a == goodsr.count():
                    return render(request, 'sop/goods_record.html', {'goods': goods,
                                                                     'user': user,
                                                                     'all_rmb': sum(list_1),
                                                                     'pages': pages})


def record_next(request, user_id, pages):
    user = Users.objects.get(pk=user_id)
    goodsr = Deal_goods.objects.filter(goods_user=user)
    pages = int(pages)

    if pages < goodsr.count() / 4:
        pages = pages + 1
        goods = Deal_goods.objects.filter(goods_user=user)[(pages-1)*4:pages*4]
        a = 0
        list_1 = []
        for i in goodsr:
            a = a + 1
            e = int(i.goods_price) * i.goods_stock
            print(e)
            list_1.append(e)
            if a == goodsr.count():
                print(sum(list_1))
                return render(request, 'sop/goods_record.html', {'goods': goods,
                                                                 'user': user,
                                                                 'all_rmb': sum(list_1),
                                                                 'pages': pages})
    else:
        goods = Deal_goods.objects.filter(goods_user=user)[(pages - 1) * 4:pages * 4]
        a = 0
        list_1 = []
        for i in goodsr:
            a = a + 1
            e = int(i.goods_price) * i.goods_stock
            list_1.append(e)
            if a == goodsr.count():
                return render(request, 'sop/goods_record.html', {'goods': goods,
                                                                 'user': user,
                                                                 'all_rmb': sum(list_1),
                                                                 'pages': pages})


def cart(request, user_id, pages):
    pages = int(pages)
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.get(pk=request.POST['goods_id'])
    goods_all = Goods.objects.filter(goods_state='已上架')[(pages-1)*4:pages*4]
    if request.POST['stock'] and request.POST['stock'].isdigit():
        Cart.objects.create(goods_name=goods.goods_name,
                            goods_price=goods.goods_price,
                            goods_x=request.POST['stock'],
                            goods_user=user,
                            goods_id=goods.goods_id)
        return render(request, 'sop/shop.html', {'user': user,
                                                 'goods': goods_all,
                                                 'succeed': '添加成功！',
                                                 'pages': pages})
    else:
        return render(request, 'sop/shop.html', {'user': user,
                                                 'goods': goods_all,
                                                 'succeed': '请输入你要添加的数量',
                                                 'pages': pages})


def show_cart(request, user_id):
    user = Users.objects.get(pk=user_id)
    cart = Cart.objects.filter(goods_user=user)
    if cart:
        a = 0
        list_1 = []
        for i in cart:
            a = a+1
            r = int(i.goods_price) * i.goods_x
            list_1.append(r)
            if a == cart.count():
                return render(request, 'sop/show_cart.html', {'cart': cart,
                                                              'user': user,
                                                              'all_rmb': sum(list_1), })
    else:
        return render(request, 'sop/show_cart.html', {'cart': cart,
                                                      'user': user,
                                                      'succeed': '这里空空如也'
                                                      })


def close(request, user_id):
    user = Users.objects.get(pk=user_id)
    cart = Cart.objects.filter(goods_user=user)
    a = 0
    if cart:
        for i in cart:
            a = a+1
            goods = Goods.objects.get(pk=i.goods_id)
            r = int(i.goods_price) * i.goods_x
            if goods.goods_stock > i.goods_x:
                if user.user_RMB > r:
                    Goods.objects.filter(pk=i.goods_id).update(goods_stock=F('goods_stock')-i.goods_x)
                    Users.objects.filter(pk=user_id).update(user_RMB=user.user_RMB-r)
                    Deal_goods.objects.create(goods_name=i.goods_name,
                                              goods_user=user,
                                              goods_id=i.goods_id,
                                              goods_price=i.goods_price,
                                              goods_stock=i.goods_x,
                                              )
                    if a == cart.count():
                        Cart.objects.filter(goods_user=user).delete()

                        return render(request, 'sop/show_cart.html', {'cart': cart,
                                                                      'user': user,
                                                                      'succeed': '购物车已清空'})

                else:
                    return render(request, 'sop/show_cart.html', {'cart': cart,
                                                                  'user': user,
                                                                  'succeed': '余额不足请充值!'})
            else:
                return render(request, 'sop/show_cart.html', {'cart': cart,
                                                              'user': user,
                                                              'succeed': '库存不足了！'})
    else:
        return render(request, 'sop/show_cart.html', {
                                                      'user': user,
                                                      'succeed': '这里空空如也,快去选择你喜欢的商品把！'})


def del_goods(request,user_id, goods_id):
    user = Users.objects.get(pk=user_id)
    Cart.objects.filter(goods_id=goods_id).delete()
    cart = Cart.objects.filter(goods_user=user)
    return render(request, 'sop/show_cart.html', {'cart': cart,
                                                  'user': user,
                                                  'succeed': '已经移除该商品'})


def del_all(request, user_id):
    user = Users.objects.get(pk=user_id)
    Cart.objects.filter(goods_id=goods_id).delete()
    return render(request, 'sop/show_cart.html', {
                                                  'user': user,
                                                  'succeed': '已清空购物车'})


def page(request, user_id, pages):
    pages = int(pages)
    user = Users.objects.get(pk=user_id)
    if pages > 1:
        pages = int(pages) - 1
        goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
        return render(request, 'sop/shop.html', {'user': user,
                                                 'goods': goods, 'pages': pages
                                                 })
    else:
        goods = Goods.objects.filter(goods_state='已上架')[0: 4]
        return render(request, 'sop/shop.html', {'user': user,
                                                 'goods': goods, 'pages': pages
                                                 })


def shop(request, user_id):
    pages = 1
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.filter(goods_state='已上架')[(pages-1) * 4: pages * 4]
    print(goods)
    return render(request, 'sop/shop.html', {'user': user,
                                             'goods': goods, 'pages': pages})


def next(request, user_id, pages):
    pages = int(pages)
    user = Users.objects.get(pk=user_id)
    goods_all = Goods.objects.filter(goods_state='已上架')
    print(goods_all.count()/4)
    if pages < goods_all.count() / 4:
        pages = pages + 1
        goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
        return render(request, 'sop/shop.html', {'user': user,
                                                 'goods': goods, 'pages': pages})
    else:
        goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
        return render(request, 'sop/shop.html', {'user': user,
                                                 'pages': pages,
                                                 'goods': goods})


def show_login(request, user_id):
    user = Users.objects.get(pk=user_id)
    login = Logins.objects.filter(user=user)
    return render(request, 'sop/show_login.html', {'user': user,
                                                   'login': login})