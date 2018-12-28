from django.shortcuts import render

# Create your views here.

from goods.models import GoodsCategory, Goods


def index(request):
    if request.method == 'GET':
        # good_category = GoodsCategory.objects.all().order_by('id')
        data = {}
        # 循环商品分类
        for cate in GoodsCategory.CATEGORY_TYPE:
            # 获取当前分类下的前四个商品信息
            goods = Goods.objects.filter(category_id=cate[0])[0:4]
            # 组装成键值对，key为商品分类的名称cate[1]，value为当前分类的商品信息goods
            data[cate[1]] = goods

        return render(request, 'index.html', {'goods_category': data})


def detail(request, id):
    if request.method == 'GET':
        # 返回商品详细信息
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods})


def list(request):
    if request.method == 'GET':
        return render(request, 'list.html')
