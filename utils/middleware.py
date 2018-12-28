from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from carts.models import ShoppingCart
from user.models import User

import re


class LoginStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 登录验证，设置全局变量(如果访问不需要登录验证的页面，如果已经登陆过，就也要设置全局变量进行展示）
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user

        if request.path == '/':
            return None

        # 在访问登录、注册、首页,购物车，media的时候不用进行下面的登录校验
        not_need_check = ['/user/login', '/user/register',
                          '/goods/index', '/carts/cart',
                          '/media/.*', '/static/.*',
                          '/goods/detail/.*',
                          '/carts/count_cart', '/carts/add_cart']
        for path in not_need_check:
            if re.match(path, request.path):
                return None

        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()  # 这两句是为了在页面上展示 ：user.username
            if not user:
                return HttpResponseRedirect(reverse('user:login'))
            # 设置全局用户对象
            request.user = user
            return None
        else:
            return HttpResponseRedirect(reverse('user:login'))


class SessionSyncMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 没有登录就不管数据同步
        # 登录情况才做数据从session同步到数据库, 且重新更新session数据

        user_id = request.session.get('user_id')
        if user_id:
            # 登录情况
            session_goods = request.session.get('goods')
            if session_goods:
                # 1. 判断session中商品是否存在于数据库中, 如果存在则更新
                # 2. 如果不存在则创建
                shop_carts = ShoppingCart.objects.filter(user_id=user_id)
                # 更新购物车中的商品数量
                data = []
                for goods in shop_carts:
                    for session_good in session_goods:
                        if session_good[0] == goods.goods_id:
                            goods.nums = session_good[1]
                            goods.is_select = session_good[2]
                            goods.save()
                            data.append(session_good[0])
                # 添加
                session_goods_ids = [i[0] for i in session_goods]
                add_goods_ids = list(set(session_goods_ids) - set(data))
                for add_goods_id in add_goods_ids:
                    for session_good in session_goods:
                        if add_goods_id == session_good[0]:
                            ShoppingCart.objects.create(user_id=user_id,
                                                        goods_id=add_goods_id,
                                                        nums=session_good[1])
            # 将数据库中数据同步到session中
            new_shop_carts = ShoppingCart.objects.filter(user_id=user_id)
            session_new_goods = [[i.goods_id, i.nums, i.is_select] for i in new_shop_carts]
            request.session['goods'] = session_new_goods
        return None
