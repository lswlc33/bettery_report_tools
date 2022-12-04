import psutil
from pynotifier import Notification
import time
import configparser
import os


def write_log(word):
    # 打开文件，打不开就创建
    try:
        f = open('record.log', 'x+')
    except FileExistsError:
        f = open('record.log', 'r+')

    f.seek(0, 2)
    f.writelines(str(word))
    f.writelines('\n')
    f.seek(0, 0)
    f.close()


def clean_log():
    try:
        f = open('record.log', 'x+')
    except FileExistsError:
        f = open('record.log', 'r+')
    # 清理log
    f.truncate()
    f.close()
    print('log清理完成')


def init_config():
    # 确认配置文件是否存在
    try:
        f = open("setting.ini")
        f.close()
        print("找到配置文件！\n"
              "(可在setting.ini里进行设置)\n"
              "**********************"
              )
    except IOError:
        # 创建配置
        config = configparser.ConfigParser()
        # 加载配置
        config['setting'] = {'sleep_time': '5',

                             }
        # 创建ini文件
        with open('setting.ini', 'w') as configfile:
            # 写入配置
            config.write(configfile)
        print("初始化应用配置完成！\n"
              "(可在setting.ini里进行设置)\n"
              "**********************")


def read_config():
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read("setting.ini", encoding='utf-8')
    dict1 = dict(config.items('setting'))
    # 返回字典
    return dict1


def logo():
    # 显示我的网址
    print("\n\n\n\n\n"
          "   ___   ___  ________  .___  ___. ____    ____ .___  ___.  __     \n"
          "   \  \ /  / |       /  |   \/   | \   \  /   / |   \/   | |  |    \n"
          "    \  V  /  `---/  /   |  \  /  |  \   \/   /  |  \  /  | |  |  \n"
          "     >   <      /  /    |  |\/|  |   \_    _/   |  |\/|  | |  |   \n"
          "    /  .  \    /  /----.|  |  |  |     |  |  __ |  |  |  | |  `----.\n"
          "   /__/ \__\  /________||__|  |__|     |__| (__)|__|  |__| |_______|"
          "\n\n\n\n\n\n"
          "              loading......"
          "\n\n"
          "              少女折寿中..."
          "\n\n"
          )


def get_status():
    # 初始化
    battery = psutil.sensors_battery()
    # 获取充电状况
    plugged = battery.power_plugged
    # 获取电量
    percent = battery.percent
    # 输出状况、电量
    return plugged, percent


def send_notice():
    # 获取电池充电状况
    a = get_status()
    plugged, percent = a
    if plugged:
        # 在充电
        notify = Notification(
            title="正在充电",
            description="请在电池模式使用本软件",
        ).send()
        a = False
        return a
    elif not plugged:
        # 不在充电
        notify = Notification(
            title="正在放电",
            description="即将开始记录，请保持后台运行",
        ).send()
        a = True
        return a
    else:
        # 看不出来在不在充电
        notify = Notification(
            title="错误",
            description="获取电池信息失败",
        ).send()
        a = False
        # 返回停止信息
        return a


def cmd_notification():
    # 获取电量
    a = get_status()
    plugged, percent = a
    # 获取时间
    t = time.strftime("%H:%M:%S", time.localtime())

    print("当前时间:" + str(t) + "  当前电量:" + str(percent) + "%")
    write_log(str(t) + "  " + str(percent))
