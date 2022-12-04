import psutil
import time
import configparser
import os
import datetime
import pyecharts.options as opts
from pyecharts.charts import Line


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
          "   \\  \\ /  / |       /  |   \\/   | \\   \\  /   / |   \\/   | |  |    \n"
          "    \\  V  /  `---/  /   |  \\  /  |  \\   \\/   /  |  \\  /  | |  |  \n"
          "     >   <      /  /    |  |\\/|  |   \\_    _/   |  |\\/|  | |  |   \n"
          "    /  .  \\    /  /----.|  |  |  |     |  |  __ |  |  |  | |  `----.\n"
          "   /__/ \\__\\  /________||__|  |__|     |__| (__)|__|  |__| |_______|"
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
        a = False
        return a
    elif not plugged:
        # 不在充电
        a = True
        return a
    else:
        # 看不出来在不在充电
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


def analyze_log():
    try:
        with open('record.log', 'r') as f:
            # 文件按照换行符分割返回列表
            data = f.read().split('\n')
            # 开始时间
            start_time = datetime.datetime.strptime(data[0].split(' ')[0], '%H:%M:%S')
            # 结束时间
            end_time = datetime.datetime.strptime(data[-2].split(' ')[0], '%H:%M:%S')
            # 获取开始电量
            start_power_state = data[0].split(' ')[2]
            # 获取结束电量
            end_power_state = data[-2].split(' ')[2]

        # 计算秒数差
        time3 = (end_time - start_time).seconds
        # 根据秒数大小自动格式化时间输出
        try:
            if 0 < time3 < 60:
                print("测试共运行时间：" + str(time3) + "秒")
            elif 60 < time3 < 3600:
                print("测试共运行时间：" + str(time3 // 60) + "分钟")
            elif 3600 < time3:
                print("测试共运行时间：" + str(time3 // 3600) + "小时" + str(
                    (time3 // 60) - (time3 // 3600) * 60) + "分钟")
            print("期间消耗电量：" + str(int(start_power_state) - int(end_power_state)) + "%")
            speeed = ((int(start_power_state) - int(end_power_state)) / (time3 // 60)) * 60
            print("耗电速度：" + str(round(speeed, 2)) + "%/小时")
            xu_hang = 100 / (((int(start_power_state) - int(end_power_state)) / (time3 // 60)) * 60)
            print("预计续航：" + str(round(xu_hang, 2)) + "小时")
        except ZeroDivisionError:
            print("预计续航：数据不足/过短")
        if input("按任意键按返回\n") == "":
            pass
    except FileNotFoundError:
        print("错误！log文件不存在")
        if input("按任意键按返回\n") == "":
            pass


def analyze_report():
    os.system('cls')
    print("\n\n\n")
    print("log分析报告")
    analyze_log()


def record_data():
    os.system('cls')
    init_config()
    while True:
        if input("回车以开始程序\n") == "":
            pass
        # 给你发个通知
        a = send_notice()
        clean_log()
        if not a:
            # 终端清屏
            os.system('cls')
            # 不在放电测试什么续航啊
            print("充电中 或 获取数据失败"
                  "\n即将退出. . .")
            exit()
        else:
            # 终端清屏
            os.system('cls')
            # 循环输出电池电量信息
        try:
            while True:
                cmd_notification()
                a = read_config()
                time.sleep(int(a['sleep_time']))
        except ValueError:
            print("配置文件错误")
            if input("按任意键按退出\n") == "":
                pass


def create_charts():
    os.system('cls')
    print("\n\n\n")

    try:
        with open('record.log', 'r') as f:
            # 文件按照换行符分割返回列表
            data = f.read().split('\n')
        line_num = len(open(r"record.log", 'r').readlines())
        print("获取到" + str(line_num) + "条记录")
        seconds = []
        for i in range(1, int(line_num) + 1):
            start_time = datetime.datetime.strptime(data[line_num - i].split(' ')[0], '%H:%M:%S')
            end_time = datetime.datetime.strptime(data[-2].split(' ')[0], '%H:%M:%S')
            time3 = (end_time - start_time).seconds
            seconds.append(str(time3) + "s")
        print("生成了" + str(len(seconds)) + "条时间数据")
        state = []
        for i in range(0, int(line_num)):
            power_state = data[i].split(' ')[2]
            state.append(power_state)
        print("生成了" + str(len(state)) + "条电量数据")
        line_base = (
            Line()
            .add_xaxis(seconds)
            .add_yaxis("电量(单位：%)", state)
            .set_global_opts(title_opts=opts.TitleOpts(title="电量统计折线图",
                                                       pos_left="center"),
                             legend_opts=opts.LegendOpts(is_show=True, pos_right="10%", pos_top="10%",
                                                         orient='vertical')
                             )
        )

        line_base.render('电量图表.html')
        print("图表已经成功输出为图表.html")
        if input("按任意键按返回\n") == "":
            pass
    except FileNotFoundError:
        print("错误！log文件不存在")
        if input("按任意键按返回\n") == "":
            pass
