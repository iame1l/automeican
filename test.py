import datetime
import random
import time
import signal

import meican.models
from meican import MeiCanLoginFail
from meican.exceptions import MeiCanError, MeiCanLoginFail, NoOrderAvailable

day_second = datetime.timedelta(days=1).total_seconds()
hours_second = datetime.timedelta(hours=1).total_seconds()

username = '@dcxt.com'
password = ''

def getNowTime():
    return int(time.time() - time.timezone) % day_second


def getZeroSeconds():
    now_t = int(time.time() - time.timezone) % day_second
    return day_second - getNowTime() % day_second


def strTime():
    return time.strftime('%Y-%m-%d,%H:%M:%S', time.localtime(time.time()))


def executeAutoOrder(m, index):
    m.load_tabs(True)
    try:
        dishes = m.list_dishes()
        limit_price = m.get_price_limit(index)
        accCount = 0
        while accCount < 100:
            dish = random.choice(dishes)
            if dish.price == limit_price:
                m.order(dish)
                print(strTime(), ' 自动下单成功, ', dish.name)
                return
            accCount = accCount + 1

    except NoOrderAvailable:
        print(strTime(), ' 已经点餐或者不开放 !')

    print('excuteAutoOrder ', index, ' time: ', strTime())


if __name__ == '__main__':
    m = None
    try:
        m = meican.MeiCan(username, password)
    except MeiCanLoginFail:
        print('用户名或者密码不正确')
        exit(0)

    print(strTime(), ' 开始执行 !!!! 用户名:', username)
    while True:
        m.load_tabs(True)
        time_list = m._time_list
        index = 0
        for tarTime in time_list:
            now = getNowTime()
            if now > tarTime:
                continue
            time.sleep(tarTime - now)
            executeAutoOrder(m, index)
            index = index + 1

        print(strTime(), ' 今日自动下单结束 !')
        time.sleep(getZeroSeconds() + 1 * hours_second)
