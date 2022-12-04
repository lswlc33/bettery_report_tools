"""
求求你使用windows终端运行本脚本（不要用编辑器）
项目：笔记本电池助手
作者：雪中明月
日期：2022/11/21
目标：
1. 获取电池信息(done)
2. 终端输出(done)
3. ini配置文件(done)
4. log日志文件(done)
5. 分析log，生成报告
6. 图表生成
7. 图片导出
8. UI制作
"""
import psutil
from pynotifier import Notification
import time
import configparser
import os
import b_lib

# 主循环代码
if __name__ == "__main__":
    b_lib.logo()
    time.sleep(2)
    # 终端清屏
    os.system('cls')
    b_lib.init_config()
    while True:
        if input("回车以开始程序") == "":
            # 给你发个通知
            a = b_lib.send_notice()
            b_lib.clean_log()
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
                while True:
                    b_lib.cmd_notification()
                    a = b_lib.read_config()
                    time.sleep(int(a['sleep_time']))
        os.system('cls')
