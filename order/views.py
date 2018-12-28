from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from carts.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from utils.functions import get_order_sn


def place_order(request):
    if request.method == 'GET':
        # 从数据库中取数据（这个页面需要登录才能访问）
        user_id = request.session.get('user_id')
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)

        # 给购物车物品添加小计价格属性
        all_total = 0
        for carts in shop_carts:
            price = carts.nums * carts.goods.shop_price
            carts.total = price
            all_total += price

        # 结算商品个数，总价
        carts_count = len(shop_carts)

        return render(request, 'place_order.html', {'shop_carts': shop_carts, 'carts_count': carts_count, 'all_total': all_total})


def make_order(request):
    if request.method == 'GET':
        # 创建订单
        # 创建订单详情
        # 购物车删除已经下单的商品
        user_id = request.session['user_id']
        # 取购物车中勾选的商品
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)
        # 计算下单的总价
        order_mount = 0
        for carts in shop_carts:
            order_mount += carts.nums * carts.goods.shop_price
        # 生成订单交易号
        order_sn = get_order_sn()
        # 创建订单
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount)

        # 创建订单详情
        for carts in shop_carts:
            OrderGoods.objects.create(order=order,
                                      goods=carts.goods,
                                      goods_nums=carts.nums)
        # 删除购物车中的商品
        shop_carts.delete()
        request.session.pop('goods')
        return JsonResponse({'code': 200, 'msg': '请求成功'})
