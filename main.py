"""
求求你使用windows终端运行本脚本（不要用编辑器）
项目：笔记本电池助手
作者：雪中明月
日期： 2022/11/21
目标：
1. 获取电池信息(done)
2. 终端输出(done)
3. ini配置文件(done)
4. log日志文件(done)
5. 分析log,生成报告(done)
6. 图表生成(done)
7. 图片导出
8. UI制作
"""
from b_lib import *

# 主循环代码
if __name__ == "__main__":
    logo()
    time.sleep(2)
    # 终端清屏
    while True:
        os.system('cls')
        print("功能一览"
              "\n\n\n"
              "1.数据收集\n"
              "2.记录分析\n"
              "3.图表导出\n"
              "4."
              "\n\n")
        a = input("你的选择：\n")
        if a == "1":
            record_data()
        elif a == "2":
            analyze_report()
        elif a == "3":
            create_charts()
        elif a == "4":
            pass
