from django.conf.urls import url

from carts import views

urlpatterns = [
    url(r'^cart', views.cart, name='cart'),
    # 加入购物车
    url(r'^add_cart', views.add_cart, name='add_cart'),
    url(r'^count_cart', views.count_cart, name='count_cart'),
    url(r'^change_cart', views.change_cart, name='change_cart'),
    # url(r'^select_goods_cart', views.select_goods_cart, name='select_goods_cart'),

]