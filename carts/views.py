from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from goods.models import Goods


def cart(request):
    if request.method == 'GET':
        # 返回购物车中的数据，不用区分登录和没有登录的情况
        # 因为所有数据只需要从session中取值即可
        session_goods = request.session.get('goods')
        data = []
        if session_goods:
            for se_goods in session_goods:
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                nums = se_goods[1]
                price = goods.shop_price * se_goods[1]
                is_select = se_goods[2]
                data.append([goods, nums, price, is_select])

        # 需要将结构返回给页面
        # [[商品对象，商品数量，商品价格],[商品对象，商品数量，商品价格]]
        return render(request, 'cart.html', {'goods_all': data, 'goods_cart_count': len(data)})


def add_cart(request):
    if request.method == 'POST':
        # 保存到session中
        # 1.获取前端ajax提交商品goods_id,商品数量nums
        # 2.组装储存到session中的数据结构
        # [[goods_id, nums, is_select], [goods_id, nums, is_select]...]
        # 3.如果加入到session中的商品已经存在session中，则更新nums字段

        goods_id = int(request.POST.get('goods_id'))   # 别忘了将这个字符串类型转换成int类型，下面才能加减
        nums = int(request.POST.get('nums'))
        # 组装储存的结构[商品id, 商品数量, 选择状态]
        goods_list = [goods_id, nums, 1]
        # 判断session是否保存了购物车数据
        # {'goods': [[id, num, 1], [id, num, 1]]}
        session_goods = request.session.get('goods')
        if session_goods:
            # 修改
            flag = False
            for goods in session_goods:
                # goods为[goods_id, nums, is_select]
                if goods[0] == goods_id:
                    goods[1] += nums
                    flag = True
            # 添加
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods   # session_goods只是自己定义的一个中间容器，在添加或者更新后，要同步给缓存
            # session中保存的商品个数
            goods_count = len(request.session['goods'])

        else:
            # 第一次添加数据到session中，保存键值对
            # 键为goods，值为[[goods_id, nums, is_select]]
            request.session['goods'] = [goods_list]
            goods_count = len(request.session['goods'])

        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'goods_count': goods_count
                             })


def count_cart(request):
    if request.method == 'GET':
        # [[goods_id, nums, is_select], [goods_id, nums, is_select]...]
        session_goods = request.session.get('goods')
        count = len(session_goods) if session_goods else 0
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'count': count
                             })


def change_cart(request):
    if request.method == 'POST':
        # 获取前端ajax传递的goods_id,is_select,nums
        goods_id = int(request.POST.get('goods_id'))
        is_select = request.POST.get('is_select')
        nums = int(request.POST.get('nums'))
        # 前后端的true/false不一样注意转换
        if is_select == 'true':
            is_select = True
        else:
            is_select = False
        # 获取session中的商品信息
        session_goods = request.session.get('goods')
        for goods in session_goods:
            # goods:[goods_id, nums, is_select]
            if goods_id == goods[0]:
                # 根据用户对购物车中的操作（数量加减和是否勾选），修改session中的商品数量和选择状态
                goods[1] = int(nums) if nums else goods[1]
                goods[2] = is_select
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


# def select_goods_cart(request):
#      if request.method == 'GET':
#         # 计算被选的商品数量和总价
#         session_goods = request.session.get('goods')
#
#         selected_goods = []
#         selected_count = 0
#         total_money = 0
#         for goods in session_goods:
#             if goods[2]==True:
#                 selected_goods.append(goods[0])
#                 total_money +=
#                 selected_count += 1
#         return JsonResponse({'code': 200, 'msg': '请求成功', 'selected_goods': selected_goods})


