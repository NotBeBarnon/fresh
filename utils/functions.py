
import random

# 生成订单交易号
import time


def get_order_sn():
    s='1234567890zaqwsxcderfvbgtyhnmjuiklopZAQWSXCDERFVBGTYHNMJUIKLOP'
    order_sn = ''
    for _ in range(20):
        order_sn += random.choice(s)
    order_sn += time.time()
    return order_sn