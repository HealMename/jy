from django.shortcuts import render,reverse
from .models import *
import time
import math
import random
from django.db.models import F
import hashlib
import os
from django.conf import settings
from .forms import Login, Register, Yue, Add_goods, Carts, UserImg
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def handle(user_id, user_head, ext):
    user = Users.objects.get(pk=user_id)
    file_name = user.user_account + ext
    file_path = os.path.join(settings.BASE_DIR, 'sop/static/', file_name)
    print(file_path)
    with open(file_path, 'wb+') as u:
        for s in user_head.chunks():
            u.write(s)


def upload(request):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    if request.method == 'POST':
        user_head = request.FILES
        if len(user_head) > 0:
            ext = os.path.splitext(user_head['user_head'].name)[1]
            handle(user.id, user_head['user_head'], ext)
            return render(request, 'sop/user_xx.html', {'user_xx': user, 'succeed': '上传成功'})
        else:
            return render(request, 'sop/user_xx.html', {'user_xx': user, 'succeed': '上传失败'})


def home(request):
    context = dict()
    user = Users.objects.get(pk=3)
    goods = Goods.objects.filter(goods_user=user)
    context['goods'] = goods
    print(goods)
    if request.session.get('user_id'):
        user = Users.objects.get(pk=request.session['user_id'])
        context['user_id'] = user
        return render(request, 'sops/index.html', context)
    else:

        return render(request, 'sops/index.html', context)


def homes(request):
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        user = Users.objects.get(pk=user_id)
        Logins.objects.create(logout='退出', user=user)
        del request.session['user_id']
        return HttpResponseRedirect('/sop/index/')
    return HttpResponseRedirect('/sop/index/')


def zc(request):
    form = Register()
    code = str(random.randint(0, 9))+str(chr(random.randrange(65, 90))*3)
    return render(request, 'sops/register.html', {'code': code, 'form': form})


def register(request, code):
    form = Register(request.POST)
    user = Users.objects.filter(user_account=request.POST['user_account']).exists()
    if form.is_valid():
        if code == request.POST['code']:
            if not user:
                md5 = hashlib.md5()
                salt = '!!qwhrkjqhr'
                md5.update(request.POST['user_password'].encode('utf8'))
                md5.update(salt.encode('utf8'))
                password = md5.hexdigest()
                form.cleaned_data['user_password'] = password
                form = Register(form.cleaned_data)
                form.save()
                user = Users.objects.get(user_account=request.POST['user_account'])
                request.session['user_id'] = user.id
                request.session.set_expiry(0)
                Logins.objects.create(logout='登录', user=user)
                return HttpResponseRedirect(reverse('sop:home'))
            else:
                code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
                return render(request, 'sops/register.html', {'code': code, 'nots': '该账号已存在', 'form': form})
        else:
            code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
            return render(request, 'sops/register.html', {'code': code, 'nots': '验证码错误', 'form': form})
    else:
        code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
        return render(request, 'sops/register.html', {'code': code, 'form': form, 'nots': '不通过'})


def login(request):
    login = Login()
    code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
    return render(request, 'sops/login.html', {'code': code, 'form': login})


def lo(request, code):
    form = Login(request.POST)
    if form.is_valid():
        if code == request.POST['code']:
                md5 = hashlib.md5()
                salt = '!!qwhrkjqhr'
                md5.update(request.POST['password'].encode('utf8'))
                md5.update(salt.encode('utf8'))
                password = md5.hexdigest()
                user = Users.objects.filter(user_account=request.POST['account']).filter(user_password=password).exists()
                if user:
                    users = Users.objects.get(user_account=request.POST['account'])
                    Logins.objects.create(user=users)
                    request.session['user_id'] = users.id
                    request.session.set_expiry(0)
                    print(request.session['user_id'])
                    return HttpResponseRedirect(reverse('sop:home'))
                else:
                    code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
                    return render(request, 'sops/login.html', {'code': code, 'not_code': '账号或密码不存在\n 请重试！'})
        else:
            code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
            return render(request, 'sops/login.html', {'code': code, 'not_code': '验证码错误！'})
    else:
        code = str(random.randint(0, 9)) + str(chr(random.randrange(65, 90)) * 3)
        return render(request, 'sops/login.html', {'code': code, 'form': form})


def update_password(request):
    if request.session.get("user_id"):
        user = Users.objects.get(pk=request.session['user_id'])
        return render(request, 'sop/update_password.html', {'user': user})
    else:
        print("未登录")


def passwords(request):
    user = Users.objects.get(pk=request.session['user_id'])
    if user.user_answer == request.POST['answer']:
        md5 = hashlib.md5()
        salt = '!!qwhrkjqhr'
        md5.update(request.POST['passwords'].encode('utf8'))
        md5.update(salt.encode('utf8'))
        password = md5.hexdigest()
        user.user_password = password
        user.save()
        return render(request, 'sop/update_password.html', {'new': '修改成功', 'user': user})
    else:
        return render(request, 'sop/update_password.html', {'user': user, 'posswords': '密报问题错误'})


def user_xx(request):
    form = UserImg()
    user = Users.objects.get(pk=request.session['user_id'])
    if request.method == 'POST':
        user_head = request.FILES
        if len(user_head) > 0:
            ext = os.path.splitext(user_head['user_head'].name)[1]
            handle(user.id, user_head['user_head'], ext)
            return render(request, 'sops/user_xx.html', {'user_id': user, 'succeed': '上传成功',
                                                         'form': form})
        else:
            return render(request, 'sops/user_xx.html', {'user_id': user, 'succeed': '上传失败',
                                                         'form': form})

    return render(request, 'sops/user_xx.html', {'user_id': user, 'form': form})


def log(request):
    return render(request, 'sop/goods.html', {'users': request.session['user_id']})


def yue(request):
    form = Yue()
    user = Users.objects.get(pk=request.session['user_id'])
    if request.method == "POST":
        form = Yue(request.POST)
        if form.is_valid():
            user_RMB = int(request.POST['user_RMB'])
            Users.objects.filter(pk=user.id).update(user_RMB=F('user_RMB')+user_RMB)
            user = Users.objects.get(pk=user.id)
            Admins.objects.create(water='收入', detail=user_RMB)
            return render(request, 'sops/yue.html', {'user_id': user, 'succeed': '充值成功', 'form': form})

    return render(request, 'sops/yue.html', {'user_id': user, 'form': form, 'succeed': '正在充值'})


def toup(request):
    user_id = request.session['user_id']
    Users.objects.filter(pk=request.session['user_id']).update(user_RMB=request.POST['rmb']+F('user_RMB'))
    water = request.POST['rmb']
    Admins.objects.create(water='收入', detail=water)
    return render(request, 'sop/goods.html', {'users': user_id})


def manage(request):
    return render(request, 'sop/user_goods.html', {'user_id': request.session['user_id']})


def add_goods(request):
    form = Add_goods()
    return render(request, 'sops/add_goods.html', {'user_id': request.session['user_id'], 'form': form})


def handle_uploaded_file(file_obj, goods_id, ext):

    filename = "%s%s" % (goods_id, ext)
    file_path = os.path.join(settings.BASE_DIR, 'sop/static/goods_img', filename)
    print(file_path)
    with open(file_path, 'wb+') as f:
        for chunk in file_obj.chunks():
            print(chunk)
            f.write(chunk)


def add_goods_add(request):
    tim = math.ceil(time.time())
    user = Users.objects.get(id=request.session['user_id'])
    files = request.FILES
    form = Add_goods(request.POST, request.FILES)
    # is_valid()方法用于验证提交的数据是否符合Form类的字段定义
    if form.is_valid():

        goods = Goods.objects.create(goods_name=request.POST['goods_name'],
                                     goods_id=request.POST['goods_class'] + str(tim) + str(random.randint(1, 10)) * 6,
                                     goods_price=request.POST['goods_price'],
                                     goods_class=request.POST['goods_class'],
                                     goods_stock=request.POST['goods_stock'],
                                     goods_user=user,
                                     goods_update=timezone.now(),
                                     )

        file_obj = files['goods_img']
        file_obj_2 = files['goods_music']
        ext = os.path.splitext(file_obj.name)[1]
        ext_2 = os.path.splitext(file_obj_2.name)[1]
        Goods.objects.filter(pk=goods.goods_id).update(goods_img='goods_img/'+goods.goods_id+ext,
                                                       goods_music='goods_img/'+goods.goods_id+ext_2)
        handle_uploaded_file(file_obj, goods.goods_id, ext)
        handle_uploaded_file(file_obj_2, goods.goods_id, ext_2)

        print(goods.goods_id)
        Update.objects.create(goods_id=goods.goods_id,
                              goods_text='添加了'+request.POST['goods_name']+'商品',
                              goods_user=user)
        return render(request, 'sops/add_goods.html', {'from': form, 'succeed': '添加成功'})

    else:
        return render(request, 'sops/add_goods.html', {'form': form, 'succeed': '请重试2'})


def ll(request):
    page = 1
    user = Users.objects.get(pk=request.session['user_id'])
    user_goods = Goods.objects.filter(goods_user_id=user).order_by('goods_stock')
    return render(request, 'sops/user_goodsall.html', {'user_goods': user_goods,
                                                       'user_id': user, 'page': page})


def up_ll(request, page):
    user_id = request.session['user_id']
    page = int(page)
    if page == 1:
        user = Users.objects.get(pk=user_id)
        user_goods = Goods.objects.filter(goods_user_id=user).order_by('goods_stock')[(page-1)*4:page*4]
        return render(request, 'sop/user_goodsall.html', {'user_goods': user_goods,
                                                          'user': user, 'page': page})
    else:
        page -= 1
        user = Users.objects.get(pk=user_id)
        user_goods = Goods.objects.filter(goods_user_id=user).order_by('goods_stock')[(page - 1) * 4:page * 4]
        return render(request, 'sop/user_goodsall.html', {'user_goods': user_goods,
                                                          'user': user, 'page': page})


def down_ll(request, page):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    page = int(page)
    goods = Goods.objects.filter(goods_user_id=user)
    if page == goods.count()/4:

        user_goods = Goods.objects.filter(goods_user_id=user).order_by('goods_stock')[(page-1)*4:page*4]
        return render(request, 'sop/user_goodsall.html', {'user_goods': user_goods,
                                                          'user': user, 'page': page})
    else:
        page += 1
        user_goods = Goods.objects.filter(goods_user_id=user).order_by('goods_stock')[(page - 1) * 4:page * 4]
        return render(request, 'sop/user_goodsall.html', {'user_goods': user_goods,
                                                          'user': user, 'page': page})


def goods_z(request):
    return render(request, 'sop/goods_z.html', {'user_id': request.session['user_id']})


def goods_id(request):
    goods_id = request.POST['goods_id']
    goods = Goods.objects.filter(goods_delete='0').filter(goods_id=goods_id)
    if goods:
        return render(request, 'sop/goods_z.html', {'user_id': request.session['user_id'],
                                                    'goods_id': goods[0]})
    else:
        return render(request, 'sop/goods_z.html', {'user_id': request.session['user_id'],
                                                    'goods_id': goods[0], 'goods_ex': '该商品不存在或已被删除'})


def update_goods(request, goods_id):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.get(pk=goods_id)
    return render(request, 'sops/update_goods.html', {'goods': goods,
                                                      'user_id': user})


def update_goo(request):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.get(pk=request.POST['update_goods'])
    return render(request, 'sop/update_goo.html', {'user': user,
                                                   'goods': goods
                                                   })


def update(request):
    user_id = request.session['user_id']
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


def all_update(request):
    user_id = request.session['user_id']
    user = Users.objects.get(id=user_id)
    goods_update = Update.objects.filter(goods_user=user)
    return render(request, 'sop/all_update.html', {'goods_update': goods_update,
                                                   'user': user})


def state(request, goods_id):
    user_id = request.session['user_id']
    Goods.objects.filter(goods_id=goods_id).update(goods_state='已上架')
    goods = Goods.objects.filter(goods_user_id=user_id).order_by('goods_stock')
    user = Users.objects.get(pk=user_id)
    return render(request, 'sops/user_goodsall.html', {'user_id': user,
                                                       'user_goods': goods})


def cancel(request, goods_id):
    user_id = request.session['user_id']
    Goods.objects.filter(goods_id=goods_id).update(goods_state='未上架')
    goods = Goods.objects.filter(goods_user_id=user_id).order_by('goods_stock')
    user = Users.objects.get(pk=user_id)
    return render(request, 'sops/user_goodsall.html', {'user_id': user,
                                                       'user_goods': goods})


def goods_record(request):
    user_id = request.session.get('user_id')
    if user_id:
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
    else:
        return HttpResponseRedirect(reverse('sop:home'))


def record_pages(request, pages):
    user_id = request.session['user_id']
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


def record_next(request, pages):
    user_id = request.session['user_id']
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


def cart(request, goods_id):
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        user = Users.objects.get(pk=user_id)
        goods = Goods.objects.get(pk=goods_id)
        if 1 < goods.goods_stock:
            if not Cart.objects.filter(goods_id=goods_id).filter(goods_user=user).exists():
                Cart.objects.create(goods_name=goods.goods_name,
                                    goods_price=goods.goods_price,
                                    goods_x=1,
                                    goods_user=user,
                                    goods_id=goods.goods_id,
                                    goods_img=goods.goods_img)

                goods.save()
                return render(request, 'sops/xx.html', {'succeed': '添加成功！'})
            else:
                Cart.objects.filter(goods_id=goods_id).update(goods_x=F('goods_x')+1)
                return render(request, 'sops/xx.html', {'succeed': '添加成功！'})
        else:
            return render(request, 'sops/xx.html', {'succeed': '库存不足'})
    else:
        return HttpResponseRedirect(reverse('sop:show_cart'))


def show_cart(request):
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        print(user_id)
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
                    return render(request, 'sops/cart.html', {'cart': cart,
                                                              'user_id': user,
                                                              'all_rmb': sum(list_1), })
        else:
            return render(request, 'sops/cart.html', {'cart': cart,
                                                      'user_id': user,
                                                      'succeed': '这里空空如也'})
    else:
        return render(request, 'sops/cart.html', {'succeed': '这里空空如也'})


def close(request):
    if request.session.get('user_id'):
        user_id = request.session['user_id']
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
                        Users.objects.filter(goods=goods).update(user_RMB=F('user_RMB') + i.goods_price*i.goods_x)
                        seller = Users.objects.get(goods=goods)
                        User_bill.objects.create(water='收入',
                                                 detail=i.goods_price*i.goods_x,
                                                 user_name=seller)
                        User_bill.objects.create(water='支出',
                                                 detail=i.goods_price*i.goods_x,
                                                 user_name=user)
                        if a == cart.count():
                            Cart.objects.filter(goods_user=user).delete()
                            user = Users.objects.get(pk=user.id)
                            return render(request, 'sops/cart.html', {'user_id': user,
                                                                      'succeed': '购物车已清空'})

                    else:
                        cart = Cart.objects.filter(goods_user=user)
                        return render(request, 'sops/cart.html', {'cart': cart,
                                                                  'user_id': user,
                                                                  'succeed': '余额不足请充值!'})
                else:
                    cart = Cart.objects.filter(goods_user=user)
                    return render(request, 'sops/cart.html', {'user_id': user, 'cart': cart,
                                                              'succeed': '库存不足了！'})
        else:
            return render(request, 'sops/cart.html', {'user_id': user,
                                                      'succeed': '这里空空如也,快去选择你喜欢的商品把！'})
    else:
        return HttpResponseRedirect(reverse('sop:show_cart'))


def del_goods(request, goods_id):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    Cart.objects.filter(goods_id=goods_id).delete()
    cart = Cart.objects.filter(goods_user=user)
    return render(request, 'sops/cart.html', {'cart': cart,
                                              'user_id': user,
                                              'succeed': '已经移除该商品'})


def del_all(request):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    Cart.objects.filter(goods_id=goods_id).delete()
    return render(request, 'sop/show_cart.html', {
                                                  'user_id': user,
                                                  'succeed': '已清空购物车'})


def page(request, pages):
    pages = int(pages)
    if request.session.get('user_id'):
        user_id = request.session['user_id']


        user = Users.objects.get(pk=user_id)
        if pages > 1:
            pages = int(pages) - 1
            goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
            return render(request, 'tages/page.html', {'user_id': user,
                                                          'goods': goods, 'pages': pages
                                                     })
        else:
            goods = Goods.objects.filter(goods_state='已上架')[0: 4]
            return render(request, 'tages/page.html', {'user_id': user,
                                                          'goods': goods, 'pages': pages
                                                     })
    else:
        goods = Goods.objects.filter(goods_state='已上架')[0: 4]
        return render(request, 'tages/page.html', {'goods': goods, 'pages': pages
                                                   })



def shop(request):
    pages = 1
    goods = Goods.objects.filter(goods_state='已上架')[0:4]
    print(goods)

    if request.session.get('user_id'):
        user_id = request.session['user_id']
        user = Users.objects.get(pk=user_id)
        return render(request, 'sops/products.html', {'user_id': user, 'goods': goods, 'pages': pages})
    else:
        return render(request, 'sops/products.html', {'goods': goods, 'pages': pages})


def next(request, pages):
    goods_all = Goods.objects.filter(goods_state='已上架')
    pages = int(pages)
    if request.session.get('user_id'):
        user_id = request.session['user_id']


        user = Users.objects.get(pk=user_id)

        print(goods_all.count()/4)
        if pages < goods_all.count() / 4:
            pages = pages + 1
            goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
            return render(request, 'tages/page.html', {'user_id': user,
                                                          'goods': goods, 'pages': pages})
        else:
            goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
            return render(request, 'tages/page.html', {'user_id': user,
                                                          'pages': pages,
                                                          'goods': goods})
    else:
        pages = pages + 1
        goods = Goods.objects.filter(goods_state='已上架')[(pages - 1) * 4: pages * 4]
        return render(request, 'tages/page.html', {
                                                   'pages': pages,
                                                   'goods': goods})



def show_login(request):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    login = Logins.objects.filter(user=user)
    return render(request, 'sops/show_login.html', {'user_id': user,
                                                    'login': login})