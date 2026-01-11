import time
import os
import sys
import winreg

import pyautogui

from pathlib import Path

from datetime import datetime

from PySide6.QtWidgets import QApplication,QButtonGroup,QHBoxLayout,QRadioButton,QPlainTextEdit,QTextEdit,QStyle,QWidget,QToolBox, QMainWindow,QPushButton,QLabel,QLineEdit,QComboBox,QVBoxLayout
from PySide6.QtCore import Qt, QObject,QThread,Signal
from PySide6.QtGui import QIcon

#其他自己写的文件
import click_behavior
import click_action


# pyinstaller.exe -D -i main.ico  main.py
#这个是导出用的

#不知道干啥的，gpt要我写的，说是能缓解导入到其他设备的问题
if getattr(sys, "frozen", False):
    os.environ["OPENCV_SKIP_PYTHON_LOADER"] = "1"

#各种全局变量
#这是任务的1的意思
guaji_1=3#刷link raid

#挂机选择的等级，默认是6，和选择框相同
link_raid_lv_choice = 6

#link raid喝体力药的次数 1是不喝药，4是喝三次，要多一次
link_raid_lp_recover_times=1

#这是任务的2的意思
guaji_2=3#刷圣遗物

#圣遗物喝体力药的次数 1是不喝药，4是喝三次，要多一次
crystalis_lp_recover_times=9



class mywindow(QWidget):
    def __init__(self):
        global link_raid_lv_choice
        global link_raid_lp_recover_times
        super().__init__()

        #左上角页面名字
        self.setWindowTitle('圆哆啦挂机器')
        #图标
        self.setWindowIcon(QIcon('./aim/resource/main.ico'))
        #窗体尺寸
        self.resize(300,600)

        #框体顶部的提示
        self.textedit_1_title = QLabel('输出运行结果的框框')
        # 用于输出运行日志的框体
        self.textedit_1=QPlainTextEdit()

    #各种进程
        #用于停止的进程
        self.thread_stop= stop_any()

        #刷raid进程
        self.workthread_1 = WorkThread_1()
        self.workthread_1.signal.connect(lambda x :self.textedit_1.appendPlainText(f"[{datetime.now().strftime('%H:%M:%S')}]: {x}"))
        # self.workthread_1.finished.connect(lambda :self.workthread_1.deleteLater()) #这一条不知道为啥加入了就无法二次启动了
        self.workthread_1.finished.connect(lambda: print('link raid挂机结束'))
        self.workthread_1.finished.connect(lambda: self.textedit_1.appendPlainText(f"[{datetime.now().strftime('%H:%M:%S')}]: link raid挂机结束或被主动停止\n"))


        self.workthread_2 = WorkThread_2()
        self.workthread_2.signal.connect(lambda x :self.textedit_1.appendPlainText(f"[{datetime.now().strftime('%H:%M:%S')}]: {x}"))
        # self.workthread_1.finished.connect(lambda :self.workthread_1.deleteLater()) #这一条不知道为啥加入了就无法二次启动了
        self.workthread_2.finished.connect(lambda: print('crystalis挂机结束'))
        self.workthread_2.finished.connect(lambda: self.textedit_1.appendPlainText(f"[{datetime.now().strftime('%H:%M:%S')}]: crystalis挂机结束或被主动停止\n"))

    #各种按钮
        #停止按钮，按下启动停止进程，会把标识符改变数值，达到停止的效果
        self.button_1=QPushButton('停下当前运行的脚本')
        self.button_1.clicked.connect(self.thread_stop.start)

        #启动link raid挂机进程
        self.button_2=QPushButton('link raid挂机启动')
        self.button_2.clicked.connect(self.workthread_1.start)

        #启动link raid挂机进程
        self.button_3=QPushButton('自动刷晶花，需要在play界面启动')
        self.button_3.clicked.connect(self.workthread_2.start)

    #link raid等级选择器

        self.group_choice_lv_label=QLabel('link raid挂机部分\n选择link raid要挂机的等级')
        #按钮和加入组别
        self.group_choice_lv = QButtonGroup(self)#等级选择的组
        self.group_choice_lv.setExclusive(True)

        self.lv_6_btn= QRadioButton('lv6')
        self.group_choice_lv.addButton(self.lv_6_btn)
        self.lv_6_btn.clicked.connect(lambda : self.change_value(6))

        self.lv_7_btn = QRadioButton('lv7')
        self.group_choice_lv.addButton(self.lv_7_btn)
        self.lv_7_btn.clicked.connect(lambda: self.change_value(7))

        self.lv_8_btn = QRadioButton('lv8')
        self.group_choice_lv.addButton(self.lv_8_btn)
        self.lv_8_btn.clicked.connect(lambda: self.change_value(8))

        self.lv_9_btn = QRadioButton('lv9')
        self.group_choice_lv.addButton(self.lv_9_btn)
        self.lv_9_btn.clicked.connect(lambda: self.change_value(9))

        self.lv_10_btn = QRadioButton('lv10')
        self.group_choice_lv.addButton(self.lv_10_btn)
        self.lv_10_btn.clicked.connect(lambda: self.change_value(10))

        self.lv_11_btn = QRadioButton('lv11')
        self.group_choice_lv.addButton(self.lv_11_btn)
        self.lv_11_btn.clicked.connect(lambda: self.change_value(11))

        self.lv_12_btn = QRadioButton('lv12')
        self.group_choice_lv.addButton(self.lv_12_btn)
        self.lv_12_btn.clicked.connect(lambda: self.change_value(12))

        self.lv_6_btn.setChecked(True)#默认选6

        #按钮的排列
        self.lv_choice_layout_1=QHBoxLayout()#横向排列
        self.lv_choice_layout_1.addWidget(self.group_choice_lv_label)#这是标识符，后面开始是按钮

        self.lv_choice_layout_2 = QHBoxLayout()  # 横向排列2
        self.lv_choice_layout_2.addWidget(self.lv_6_btn)
        self.lv_choice_layout_2.addWidget(self.lv_7_btn)
        self.lv_choice_layout_2.addWidget(self.lv_8_btn)

        self.lv_choice_layout_3 = QHBoxLayout()  # 横向排列2
        self.lv_choice_layout_3.addWidget(self.lv_9_btn)
        self.lv_choice_layout_3.addWidget(self.lv_10_btn)
        self.lv_choice_layout_3.addWidget(self.lv_11_btn)

        self.lv_choice_layout_4 = QHBoxLayout()  # 横向排列3
        self.lv_choice_layout_4.addWidget(self.lv_12_btn)

        self.lv_choice_layout_row = QVBoxLayout()  # 横向排列2
        self.lv_choice_layout_row.addLayout(self.lv_choice_layout_1)
        self.lv_choice_layout_row.addLayout(self.lv_choice_layout_2)
        self.lv_choice_layout_row.addLayout(self.lv_choice_layout_3)
        self.lv_choice_layout_row.addLayout(self.lv_choice_layout_4)

    #link raid 喝药次数选择器
        self.group_link_raid_lp_recover_label=QLabel('link raid挂机要喝体力药几次')
        #按钮和加入组别
        self.group_link_raid_lp_recover = QButtonGroup(self)#等级选择的组
        self.group_link_raid_lp_recover.setExclusive(True)

        self.lp_recover_0 = QRadioButton('不喝药')
        self.group_link_raid_lp_recover.addButton(self.lp_recover_0)
        self.lp_recover_0.clicked.connect(lambda: self.change_value_lp_recover(1))
        self.lp_recover_0.setChecked(True)

        self.lp_recover_1 = QRadioButton('1次')
        self.group_link_raid_lp_recover.addButton(self.lp_recover_1)
        self.lp_recover_1.clicked.connect(lambda: self.change_value_lp_recover(2))

        self.lp_recover_2 = QRadioButton('2次')
        self.group_link_raid_lp_recover.addButton(self.lp_recover_2)
        self.lp_recover_2.clicked.connect(lambda: self.change_value_lp_recover(3))

        self.lp_recover_3 = QRadioButton('3次')
        self.group_link_raid_lp_recover.addButton(self.lp_recover_3)
        self.lp_recover_3.clicked.connect(lambda: self.change_value_lp_recover(4))

        #体力回复次数按钮的布局
        self.link_raid_lp_recover_layout_raw = QVBoxLayout()  # 横向排列
        self.link_raid_lp_recover_layout_2=QHBoxLayout()#横向排列

        self.link_raid_lp_recover_layout_2.addWidget(self.lp_recover_0)
        self.link_raid_lp_recover_layout_2.addWidget(self.lp_recover_1)
        self.link_raid_lp_recover_layout_2.addWidget(self.lp_recover_2)
        self.link_raid_lp_recover_layout_2.addWidget(self.lp_recover_3)

        self.link_raid_lp_recover_layout_raw.addWidget(self.group_link_raid_lp_recover_label) # 这是标识符，后面开始是按钮
        self.link_raid_lp_recover_layout_raw.addLayout(self.link_raid_lp_recover_layout_2)

    #刷圣遗物界面布局器
        self.group_crystalis_lp_recover_label = QLabel('刷晶花部分\n晶花挂机要喝体力药几次')

        #按钮和加入组别
        self.group_crystalis_lp_recover = QButtonGroup(self)#回血次数选择的组
        self.group_crystalis_lp_recover.setExclusive(True)

        self.crystalis_lp_recover_0 = QRadioButton('不喝药')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_0)
        self.crystalis_lp_recover_0.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(1))

        self.crystalis_lp_recover_1 = QRadioButton('喝1次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_1)
        self.crystalis_lp_recover_1.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(2))

        self.crystalis_lp_recover_2 = QRadioButton('喝2次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_2)
        self.crystalis_lp_recover_2.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(3))

        self.crystalis_lp_recover_3 = QRadioButton('喝3次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_3)
        self.crystalis_lp_recover_3.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(4))

        self.crystalis_lp_recover_4 = QRadioButton('喝4次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_4)
        self.crystalis_lp_recover_4.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(5))

        self.crystalis_lp_recover_5 = QRadioButton('喝5次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_5)
        self.crystalis_lp_recover_5.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(6))

        self.crystalis_lp_recover_6 = QRadioButton('喝6次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_6)
        self.crystalis_lp_recover_6.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(7))

        self.crystalis_lp_recover_7 = QRadioButton('喝7次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_7)
        self.crystalis_lp_recover_7.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(8))

        self.crystalis_lp_recover_8 = QRadioButton('喝8次')
        self.group_crystalis_lp_recover.addButton(self.crystalis_lp_recover_8)
        self.crystalis_lp_recover_8.clicked.connect(lambda: self.change_value_crystalis_lp_recover_times(9))
        self.crystalis_lp_recover_8.setChecked(True)

    #刷圣遗物布局
        self.crystalis_lp_recover_layout = QVBoxLayout()

        self.crystalis_lp_recover_layout_row1 = QHBoxLayout()
        self.crystalis_lp_recover_layout_row1.addWidget(self.crystalis_lp_recover_0)
        self.crystalis_lp_recover_layout_row1.addWidget(self.crystalis_lp_recover_1)
        self.crystalis_lp_recover_layout_row1.addWidget(self.crystalis_lp_recover_2)

        self.crystalis_lp_recover_layout_row2 = QHBoxLayout()
        self.crystalis_lp_recover_layout_row2.addWidget(self.crystalis_lp_recover_3)
        self.crystalis_lp_recover_layout_row2.addWidget(self.crystalis_lp_recover_4)
        self.crystalis_lp_recover_layout_row2.addWidget(self.crystalis_lp_recover_5)

        self.crystalis_lp_recover_layout_row3 = QHBoxLayout()
        self.crystalis_lp_recover_layout_row3.addWidget(self.crystalis_lp_recover_6)
        self.crystalis_lp_recover_layout_row3.addWidget(self.crystalis_lp_recover_7)
        self.crystalis_lp_recover_layout_row3.addWidget(self.crystalis_lp_recover_8)

        self.crystalis_lp_recover_layout.addWidget(self.group_crystalis_lp_recover_label)
        self.crystalis_lp_recover_layout.addLayout(self.crystalis_lp_recover_layout_row1)
        self.crystalis_lp_recover_layout.addLayout(self.crystalis_lp_recover_layout_row2)
        self.crystalis_lp_recover_layout.addLayout(self.crystalis_lp_recover_layout_row3)
        self.crystalis_lp_recover_layout.addWidget(self.button_3)



    #主页布局
        self.mainlayout = QVBoxLayout()

        #顶部提示框
        self.mainlayout.addWidget(self.textedit_1_title)
        self.mainlayout.addWidget(self.textedit_1)
        #停止按钮
        self.mainlayout.addWidget(self.button_1)

        #先择linkraid等级，回体力次数部分
        self.mainlayout.addLayout(self.lv_choice_layout_row)
        self.mainlayout.addLayout(self.link_raid_lp_recover_layout_raw)

        #link raid挂机启动按钮
        self.mainlayout.addWidget(self.button_2)


        #圣遗物部分

        self.mainlayout.addLayout(self.crystalis_lp_recover_layout)

        self.setLayout(self.mainlayout)

    #用于改变link raid选择的等级
    def change_value(self,value_num):
        global link_raid_lv_choice
        print(f'link raid的等级修改之前是{link_raid_lv_choice}\n')
        link_raid_lv_choice=value_num
        print(f'link raid的等级变成了{value_num}\n')

    #用于改变link raid选择的等级
    def change_value_lp_recover(self,value_num):
        global link_raid_lp_recover_times
        print(f'link_raid_lp_recover_times修改之前是{link_raid_lp_recover_times}\n')
        link_raid_lp_recover_times=value_num
        print(f'link_raid_lp_recover_times的数据变成了{value_num}\n')

    # 用于改变晶花吃体力药次数
    def change_value_crystalis_lp_recover_times(self,value_num):
        global crystalis_lp_recover_times
        print(f'link_raid_lp_recover_times修改之前是{crystalis_lp_recover_times}\n')
        crystalis_lp_recover_times=value_num
        print(f'link_raid_lp_recover_times的数据变成了{value_num}\n')

class stop_any (QThread):
    def __init__(self):
        super().__init__()
        print('停止按钮准备就绪\n')

    def run(self):
        global guaji_1
        global guaji_2
        print('stop!\n')
        guaji_1= 2
        guaji_2= 2
        print(f'guaji 1这个值是{guaji_1}')
        print(f'guaji 2这个值是{guaji_2}')

class WorkThread_1 (QThread):
    signal = Signal(str)
    def __init__(self):
        super().__init__()
        print('WorkThread_1准备就绪\n')
    def run(self):
        print('执行WorkThread_1,两秒钟后启动！\n')
        self.signal.emit(str('启动link raid挂机'))


    #本自动化任务会用到的变量
        #标识符，代表这个挂机正在运行，1为正常，2为停止
        global guaji_1
        #等级选择值
        global link_raid_lv_choice
        # 体力是否够打下一把，1是可以，2是不行
        self.LP_full = 1
        # 体力药使用次数，1是不用，2是1次，最多4三次
        self.LP_full_add = link_raid_lp_recover_times
        # 找多少等级的去打
        self.level_choice = link_raid_lv_choice
        # 是否找到需要打的等级，参数为2是找到，1不是，用的点击代码就行寻找
        self.level_choice_exist = 1
        #点击play后，因为打了太多导致满了的情况，1代表没满，2代表满了
        self.join_full=1
        #找win至少运行成功一次，防止卡
        self.win_exist = 1
        #点击play之后，战斗已经结束，1代表没结束，2代表战斗已经结束
        self.already_end = 1
        #清理打满状态，指的是清理里面还有没有loss或者win状态的标识，1是清理干净了，2还没清理干净
        self.join_fill_clean =1

        guaji_1 = 1  # 这个参数代表当前任务执行符号，1为执行，2跳出


    #以下部分为正式执行内容
        self.signal.emit(str('具体挂机参数为：'))
        self.signal.emit(str(f'选择的等级是：{self.level_choice}'))
        self.signal.emit(str(f'喝体力药的次数是：{self.LP_full_add-1}'))
        self.signal.emit(str('参数错误请及时暂停'))
        self.signal.emit(str('需要在游戏主界面启动本挂机系统'))

        time.sleep(2)

        self.into_link_raid()

        while(guaji_1==1 ):

            self.link_raid_to_backup_requests()

            self.prepare_battle()#指的就是刷新一下

            self.check_join_full()#判断右下角的join是不是黑色的，黑色的说明加入对局满了

            #这里指的是清理打完的局，需要注意的是，这个参数要在没有win之后改成1，这样就跳出循环了
            self.win_exist=1#这个东西找到一次win之后变成2，否则一直等待
            while(self.join_full==2):
                self.clean_full()

            self.find_lv()

            self.join_battle()

            #判断是否结束，重新点击后会直接再次加入战斗，函数都在里面写了，不需要重新运行上面的
            self.check_already_end()

            self.battle_and_finish()

    #函数
    #从主界面到link raid界面
    def into_link_raid(self):
        result = 1

        click_action.click_position(1000, 500)
        self.signal.emit(str('把游戏弄到前台，然后随便碰一下中间'))
        time.sleep(0.2)
        click_action.click_position(1200, 600)
        self.signal.emit(str('quests点击完成，这一下使用的是位置点击，不是识图，如果没有点到说明其他问题发生了'))
        time.sleep(0.2)


        #在quest界面点击link raid
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid', 'link_raid')
            if (result ==2):
                self.signal.emit(str('link_raid点击完成'))
            else:
                self.signal.emit(str('link_raid没有找到，继续重复运行'))
        result = 1


    def link_raid_to_backup_requests(self):
        result = 1

        #进入到boss大脸的界面，在link raid界面点击backup_requests
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests', 'backup_requests')
            if (result ==2):
                self.signal.emit(str('第一层的backup_requests点击完成'))
            else:
                self.signal.emit(str('第一层的backup_requests没有找到，继续重复运行'))
        result = 1

        #点击第二层backup_requests，进入到加入界面
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/backup_requests', 'backup_requests')
            if (result ==2):
                self.signal.emit(str('第二层的backup_requests点击完成'))
            else:
                self.signal.emit(str('第二层的backup_requests没有找到，继续重复运行'))
        result = 1

    #判断右下角的join是不是黑色的，黑色的代表打满了
    def check_join_full(self):
        self.join_full = click_action.find_item_with_result(self, f'./aim/quests/link_raid/backup_requests/no_join', 'no_join')
        if (self.join_full == 1):
            self.signal.emit(str('战斗没有打满，正常运行'))
        else:
            self.signal.emit(str('战斗已经打满了，需要清理joined battles'))

        result = 1
        if(self.join_full==2) :
            # 点击左边的joined battle
            while (guaji_1 == 1 and result == 1 and self.join_full == 2):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/joined_battles',
                                                'joined_battles')
                if (result == 2):
                    self.signal.emit(str('joined_battles点击完成'))
                else:
                    self.signal.emit(str('joined_battles没有找到，继续重复运行'))
            result = 1


    def clean_full(self):
        result = 1
        find_one_win=1

        while(self.win_exist ==1):
            self.signal.emit(str(f'进入joined battle，开始清空已经结束的战斗。需要保证第一次能够清除后才会回到寻找战斗界面'))
            click_action.move_a_to_b(700, 600, 700, 200)
            click_action.move_a_to_b(700, 600, 700, 200)
            click_action.move_a_to_b(700, 600, 700, 200)
            self.signal.emit(
                str(f'完成下移，开始找结束的对局'))
            time.sleep(2)#等一下防止出问题
            find_one_win = click_action.find_item_with_result(self, './aim/quests/link_raid/joined_battles/win', 'win/lose')
            self.signal.emit(str(f'寻找win/loss的状态是{find_one_win}，1是没有了，2是还存在。此处没有找到会一直等待到找到为止，否则会无法继续'))
            if find_one_win==2:
                self.win_exist=2
            else:
                self.signal.emit(str(f'没有看到一场结束的战斗，等待5s后点击刷新，然后继续找'))
                time.sleep(5)
                result = 1

                # 点击刷新
                while (guaji_1 == 1 and result == 1):
                    result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/refresh', 'refresh')
                    if (result == 2):
                        self.signal.emit(str('refresh点击完成'))
                    else:
                        self.signal.emit(str('refresh没有找到，继续重复运行'))

        result = 1
        self.clean_fin= click_action.find_item_with_result(self, './aim/quests/link_raid/joined_battles/win', 'win/lose')
        self.signal.emit(str(f'win/loss的状态是{self.clean_fin}，1是没有了，2是还存在'))

        if (self.clean_fin==2):
            # 点击左边的joined battle，进入选择
            while (guaji_1 == 1 and result == 2):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/joined_battles',
                                                'joined_battles')
                if (result == 2):
                    self.signal.emit(str('joined_battles点击完成'))
                else:
                    self.signal.emit(str('joined_battles没有找到，继续重复运行'))
            result = 1

            # 点击win/lose
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/joined_battles/win', 'win/lose')
                if (result == 2):
                    self.signal.emit(str('win/lose点击完成'))
                else:
                    self.signal.emit(str('win/lose没有找到，继续重复运行，不应该出现这一条提示'))
            result = 1

            # 点击右下角的ended
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/joined_battles/ended', 'ended')
                if (result == 2):
                    self.signal.emit(str('ended点击完成'))
                else:
                    self.signal.emit(str('ended没有找到，继续重复运行，不应该出现这一条提示'))
            result = 1

            # 点击结算界面的tap_to_countinue
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/battle/tap_to_countinue',
                                                'tap_to_countinue')
                if (result == 2):
                    self.signal.emit(str('tap_to_countinue点击完成'))
                else:
                    self.signal.emit(str('tap_to_countinue没有找到，继续重复运行'))
            result = 1

            # 点击结算界面界面的back，点完后回到前面
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/battle/back', 'back')
                if (result == 2):
                    self.signal.emit(str('back点击完成'))
                else:
                    self.signal.emit(str('back没有找到，继续重复运行'))
            result = 1

            #返回后，点击左侧的joined battle，这个没有意义，主要是防止延迟导致出问题，如果joined battle能点击，说明加载好了
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/joined_battles',
                                                'joined_battles')
                if (result == 2):
                    self.signal.emit(str('joined_battles点击完成，这一个点击主要为了防止延迟'))
                else:
                    self.signal.emit(str('joined_battles没有找到，继续重复运行，这一个点击主要为了防止延迟'))
            result = 1

            self.clean_fin = click_action.find_item_with_result(self, './aim/quests/link_raid/joined_battles/win', 'win/lose')
            self.signal.emit(str(f'win/loss的状态是{self.clean_fin}，1是没有了，2是还存在'))

        else:
            self.join_full=1#用于跳出外部的while

            #点击第二层的backup_requests，回到选战斗界面
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/backup_requests',
                                                'backup_requests')
                if (result == 2):
                    self.signal.emit(str('第二层的backup_requests点击完成'))
                else:
                    self.signal.emit(str('第二层的backup_requests没有找到，继续重复运行'))
            result = 1

            # 点击刷新
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/refresh', 'refresh')
                if (result == 2):
                    self.signal.emit(str('refresh点击完成'))
                else:
                    self.signal.emit(str('refresh没有找到，继续重复运行'))
            result = 1


    #打架之前点击刷新
    def prepare_battle(self):
        result = 1

        #点击刷新
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/refresh', 'refresh')
            if (result ==2):
                self.signal.emit(str('refresh点击完成'))
            else:
                self.signal.emit(str('refresh没有找到，继续重复运行'))
        result = 1



    #寻找需要打架的等级，这个找不到也要继续，不能用while循环寻找
    def find_lv(self):
        # 往下拉3次用于寻找
        find_time=4
        # 这个判断对应等级是否存在，1是没找到，2是找到了默认设置没找到，进入第一次循环
        self.level_choice_exist=1;


        while(find_time>1 and self.level_choice_exist==1):
            self.level_choice_exist = click_action.find_item_with_result(self,
                                                            f'./aim/quests/link_raid/backup_requests/lv/lv{self.level_choice}/lv{self.level_choice}',
                                                            f'lv{self.level_choice}')
            if (self.level_choice_exist == 2):
                self.signal.emit(str(f'lv{self.level_choice}找到了，下一步是选择'))
            else:
                find_time=find_time-1
                self.signal.emit(str(f'lv{self.level_choice}没有找到，往下拉动，还有的寻找次数为{find_time-2}'))
                click_action.move_a_to_b(700, 600, 700, 200)
                time.sleep(4)
                self.signal.emit(str(f'往下移动完成'))

        if (self.level_choice_exist == 2):
            if (guaji_1 == 1):  # 这里不可以用while，只能运行一遍
                result = click_action.click_item_with_result(self,
                                                    f'./aim/quests/link_raid/backup_requests/lv/lv{self.level_choice}/lv{self.level_choice}',
                                                    f'lv{self.level_choice}')
                if (result == 2):
                    self.signal.emit(str(f'lv{self.level_choice}点击完成'))
                else:
                    self.signal.emit(str(f'lv{self.level_choice}没有找到，不会重复运行，理论上这一条不应该发生，即便发生了也会继续运行'))
                result = 1




        # 这个判断对应等级是否存在，1是没找到，2是找到了

        if(self.level_choice_exist==1):
            self.signal.emit(str(f'lv{self.level_choice}没有找到，直接点击第一个'))
        else:
            self.signal.emit(str(f'lv{self.level_choice}找到了，下一步是选择'))

        result =1
        #当需要点击的等级存在，点击相应等级，只过一遍，不循环，这里不会卡




    #加入战斗，需要点击join和play两个，接下来就会又各种情况判定，因为体力会满，战斗会结束
    def join_battle(self):
        global guaji_1
        result = 1

        #点击join进入到选人的界面
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/join', 'join')
            if (result ==2):
                self.signal.emit(str('join点击完成'))
            else:
                self.signal.emit(str('join没有找到，继续重复运行'))
        result = 1

        #判断体力是否耗尽，正常情况应该是1，耗尽会变成2
        time.sleep(0.2)
        self.LP_full = click_action.find_item_with_result(self, f'./aim/quests/link_raid/backup_requests/no_lp/no_lp', 'no_lp')
        self.signal.emit(str(f'体力是否耗尽的状态是{self.LP_full}，1是体力还能继续打，2是不能打了，要开始判断是否喝药或者暂停'))

        #如果体力耗尽，判断是否要结束或者喝药
        if self.LP_full==2:
            self.LP_full_add= self.LP_full_add-1
            self.signal.emit(str(f'剩余喝体力药的次数是{self.LP_full_add}，0就是不喝药了，结束挂机'))
            if self.LP_full_add==0:#剩余喝药次数耗尽
                guaji_1 = 2
            else:
                while (guaji_1 == 1 and result == 1):
                    result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/no_lp/ok', 'ok')
                    if (result == 2):
                        self.signal.emit(str('ok点击完成，完成喝药'))
                    else:
                        self.signal.emit(str('ok没有找到，继续重复运行，不应该出现这一条'))
                result = 1



        #点击play理论上进入战斗，实际上不一定，可能体力回满一类的
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/join/play', 'play')
            if (result ==2):
                self.signal.emit(str('play点击完成'))
            else:
                self.signal.emit(str('play没有找到，继续重复运行'))
        result = 1


    #这一段没有点击，无判断标识符
    def check_full(self):
        #为了防止延迟出现，这里等待3s
        time.sleep(3)
        #判断是否打满，1是没打满，默认值，2是打满
        self.join_full= click_action.find_item_with_result(self, f'./aim/quests/link_raid/backup_requests/join/full/battle_full', 'battle_full')
        if(self.join_full==1):
            self.signal.emit(str('没有打满，现在应该已经在战斗状态了'))
        else:
            self.signal.emit(str('战斗已经打满了，需要清理joined battles'))

        result = 1
        #如果说打满了，要把ok点掉，这里需要多判断一个条件
        while(guaji_1==1 and result ==1 and self.join_full==2):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/join/full/ok', 'ok')
            if (result ==2):
                self.signal.emit(str('ok点击完成'))
            else:
                self.signal.emit(str('ok没有找到，继续重复运行，这个不应该出现，出现了一定游戏出问题了！'))
        result = 1

        if(self.join_full==2):
            self.find_lv()
            self.join_battle()






    #判断是否还有win/loss，如果清理完成，回到backup request
    def check_win_clear(self):
        result = 1
        #点击左边的joined battle，这一段理论上是没用的，它是防止出现游戏延迟，直接跑到下面去运行
        while(guaji_1==1 and result ==1 and self.join_full==2):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/joined_battles', 'joined_battles')
            if (result ==2):
                self.signal.emit(str('joined_battles点击完成，这一个点击主要为了防止延迟'))
            else:
                self.signal.emit(str('joined_battles没有找到，继续重复运行，这一个点击主要为了防止延迟'))
        result = 1

        #判断是否完成清理所有的win/lose
        self.join_full= click_action.find_item_with_result(self, './aim/quests/link_raid/joined_battles/win', 'win/lose')
        self.signal.emit(str(f'win/loss的状态是{self.join_full}，1是没有了，2是还存在'))

        if(self.join_full==1):
            result = 1
            # 点击第二层backup_requests，进入到加入界面
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/backup_requests',
                                                'backup_requests')
                if (result == 2):
                    self.signal.emit(str('第二层的backup_requests点击完成'))
                else:
                    self.signal.emit(str('第二层的backup_requests没有找到，继续重复运行'))
            result = 1

            self.prepare_battle()
            self.find_lv()
            self.join_battle()



    #判断当前战斗是否结束，结束了点一下刷新
    def check_already_end(self):
        #防止延迟问题
        time.sleep(0.5)

        # 确认战斗是否结束
        self.already_end = click_action.find_item_with_result(self, f'./aim/quests/link_raid/backup_requests/join/full/already_end', 'already_end')
        self.signal.emit(str(f'战斗是否已经结束的状态是{self.already_end}，1是没有结束，2是结束了'))

        #如果战斗已经结束，点击ok，然后点击刷新
        while(self.already_end==2):
            result=1
            #点击ok
            while (guaji_1 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/join/ok', 'ok')
                if (result == 2):
                    self.signal.emit(str('ok点击完成'))
                else:
                    self.signal.emit(str('ok没有找到，继续重复运行，不应该出现这个提示'))
            result = 1

            self.prepare_battle()
            self.find_lv()
            self.join_battle()

            #再次判断，只要脸够黑，就能连着结束
            self.already_end = click_action.find_item_with_result(self, f'./aim/quests/link_raid/backup_requests/join/full/already_end', 'already_end')
            self.signal.emit(str(f'战斗是否已经结束的状态是{self.already_end}，1是没有结束，2是结束了'))

    #完成战斗，然后点back。点击战斗结束会出来的tap_to_countinue
    def battle_and_finish(self):
        result = 1

        #点击结算界面的tap_to_countinue
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/battle/tap_to_countinue', 'tap_to_countinue')
            if (result ==2):
                self.signal.emit(str('tap_to_countinue点击完成'))
            else:
                self.signal.emit(str('tap_to_countinue没有找到，战斗还在进行，继续重复运行'))
        result = 1

        #点击结算界面界面的back，点完后回到boss打脸的界面
        while(guaji_1==1 and result ==1):
            result= click_action.click_item_with_result(self, './aim/quests/link_raid/backup_requests/battle/back', 'back')
            if (result ==2):
                self.signal.emit(str('back点击完成，一场战斗结束了'))
            else:
                self.signal.emit(str('back没有找到，继续重复运行'))
        result = 1



class WorkThread_2 (QThread):
    signal = Signal(str)
    def __init__(self):
        super().__init__()
        print('WorkThread_2准备就绪\n')
    def run(self):
        print('执行WorkThread_2,两秒钟后启动！\n')
        self.signal.emit(str('启动刷晶花挂机'))

        #运行标识符，1是正常运行，2是停止
        global guaji_2
        guaji_2 =1

        #喝药次数，1是不喝药，2是1次，需要减一
        global crystalis_lp_recover_times
        self.lp_recover = crystalis_lp_recover_times

        #提示框
        self.signal.emit(str('具体参数如下：'))
        self.signal.emit(str(f'喝体力药的次数：{self.lp_recover - 1}'))
        self.signal.emit(str('参数错误请暂停'))
        self.signal.emit(str(f'需要在选择完成关卡和队伍的界面启动。也就是点一下play就进入战斗的界面'))

        time.sleep(2)
        click_action.click_position(1000, 500)
        self.signal.emit(str('把游戏弄到前台，然后随便碰一下中间'))
        time.sleep(1)

        self.click_play()
        #执行部分
        while(guaji_2==1):
            self.wait_win()
            self.click_retry_or_recover_lp()





        #函数部分
        #点击play开始挂

    def click_play(self):
        result = 1

            # 在主界面点击quests
        while (guaji_2 == 1 and result == 1):
            result = click_action.click_item_with_result(self, './aim/crystalis/play', 'play')
            if (result == 2):
                self.signal.emit(str('play点击完成'))
            else:
                self.signal.emit(str('play没有找到，请检查你所在的位置，需要在选队伍界面'))

    def wait_win(self):
        check_win=1#这东西代表看到retry，1是没看到，2是看到
        while(check_win==1 and guaji_2==1):


            #战斗结束后，右上角会出现result，点击整个右侧屏幕的任何地方几次就会让它出现retry
            result = click_action.click_item_with_result(self, './aim/crystalis/result', 'result')
            if (result == 2):
                self.signal.emit(str('result点击完成，点了之后会出现retry'))
            else:
                self.signal.emit(str('result没有找到，还在战斗状态'))

            if (result ==2):
                check_win = click_action.find_item_with_result(self, f'./aim/crystalis/retry', 'retry')
                self.signal.emit(str(f'result被点击过一次，尝试寻找retry，具体的状态是{check_win}，1是没有找到，2是找到了'))


    def click_retry_or_recover_lp(self):
        global guaji_2
        result=1
        while (guaji_2 == 1 and result == 1):
            result = click_action.click_item_with_result(self, './aim/crystalis/retry', 'retry')
            if (result == 2):
                self.signal.emit(str('retry点击完成'))
            else:
                self.signal.emit(str('retry没有找到，不应该出现这一条提示'))

        time.sleep(2) #等待确保延迟
            #寻找是否存在体力耗尽
        if(click_action.find_item_with_result(self, './aim/crystalis/ok', 'ok')==2):
            self.lp_recover=self.lp_recover-1
            self.signal.emit(str(f'体力用完了，剩余体力恢复次数还是{self.lp_recover}'))
            if(self.lp_recover==0):
                guaji_2=2

            result = 1
            while (guaji_2 == 1 and result == 1):
                result = click_action.click_item_with_result(self, './aim/crystalis/ok', 'ok')
                if (result == 2):
                    self.signal.emit(str('ok点击完成，体力完成恢复'))
                    time.sleep(5)#防止瞬间出现的retry干扰
                else:
                    self.signal.emit(str('ok没有找到，不应该出现这一条提示'))
        else:
            self.signal.emit(str(f'当前还有体力，下一把战斗正常开始，体力剩余恢复次数是{self.lp_recover-1}'))







if __name__ == '__main__':
    #这些据说能让导出程序的时候不出奇怪的bug
    def get_edge_path():
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe")
            edge_path, _ = winreg.QueryValueEx(key, "")
            winreg.CloseKey(key)
            return edge_path
        except FileNotFoundError:
            return None

    def get_executable_directory():
        if hasattr(sys, '_MEIPASS'):
            return os.path.dirname(sys.executable)  # 获取打包后可执行文件的真实路径
        else:
            return os.path.dirname(os.path.abspath(__file__))  # 获取脚本路径

    folder_path = get_executable_directory()
    print('运行路径：', folder_path)

    # 如果程序被打包为可执行文件
    if getattr(sys, 'frozen', False):
        # 获取可执行文件所在的目录
        BASE_PATH = os.path.dirname(sys.executable)
        print(f'脚本执行路径：{BASE_PATH}')
        # 将当前工作目录设置为可执行文件所在的目录
        os.chdir(BASE_PATH)
    else:
        # 如果程序作为脚本运行，使用脚本目录
        BASE_PATH = os.path.dirname(__file__)
        print(f'脚本执行路径：{BASE_PATH}')
        os.chdir(BASE_PATH)


    #这里开始是正常的pyside6的启动，前面的是据说能让导出稳定的东西
    app = QApplication([])
    window = mywindow()
    window.show()
    app.exec()






