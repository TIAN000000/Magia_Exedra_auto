import time
from pathlib import Path

import pyautogui

import click_behavior


#尝试点击一次，查询组内所有图片，返回点击结果return
def click_item_with_result(self, picture, name):
    check = 1  # 这个是判断要不要继续循环
    click_time = 1  # 尝试点击一次这玩意+1
    click_file = ''


    click_file = (f'{picture}_{click_time}.png')
    file_exist = Path(click_file)

    while (check == 1 and file_exist.exists()):
        click_file = (f'{picture}_{click_time}.png')
        click_time = click_time + 1

        file_exist=Path(click_file)
        print(f'文件状态是{file_exist}\n')

        if file_exist.exists():
            check = click_behavior.routine(click_file, name)
            print(f'点击{click_file}，点击返回值是{check}，成功点击是2，不点击是1')
            time.sleep(0.4)
        else:
            print('文件耗尽\n')

    if (check == 1):
        click_time = click_time - 1
        print(f'尝试了{click_time-1}次数，没有找到{name}，当前点击事件执行结束\n')
        return check

    if (check == 2):
        print(f'点击{name}事件完成，当前点击事件执行结束\n')
        time.sleep(0.5)
        return check



#尝试寻找目标一次，查询组内所有图片，返回寻找结果return
def find_item_with_result(self, picture, name):
    check = 1  # 这个是判断要不要继续循环
    click_time = 1  # 尝试点击一次这玩意+1
    click_file = ''

    click_file = (f'{picture}_{click_time}.png')
    file_exist = Path(click_file)

    while (check == 1 and file_exist.exists()):
        click_file = (f'{picture}_{click_time}.png')
        click_time = click_time + 1

        file_exist = Path(click_file)
        print(f'文件状态是{file_exist}\n')
        if file_exist.exists():
            check = click_behavior.routine_only_find(click_file, name)
            print(f'寻找{click_file}，寻找返回值是{check}，成功寻找是2，没找到是1')
            time.sleep(0.4)
        else:
            print('文件耗尽\n')

    if (check == 1):
        click_time = click_time - 1
        print(f'尝试了{click_time-1}次数，没有找到{name}，当前寻找事件执行结束\n')
        return check
    if (check == 2):
        print(f'寻找{name}事件完成，找到了，当前寻找事件执行结束\n')
        time.sleep(0.5)
        return check

#用于点击特定位置，输入坐标，第一个为窗口左到右的偏移，第二个上到下，注意上到下会有一个窗体厚度，不同缩放倍率会不同！
def click_position(move_lelt,move_top):
    # 把游戏窗口弄出来
    left, top = click_behavior.find_win('MadokaExedra')
    time.sleep(0.1)
    pyautogui.moveTo(left + move_lelt, top + move_top)
    time.sleep(0.1)
    pyautogui.click(left + move_lelt, top + move_top,button='left')
    time.sleep(0.1)
    return 0

def move_a_to_b(move_lelt_a,move_top_a,move_lelt_b,move_top_b):
    left, top = click_behavior.find_win('MadokaExedra')
    time.sleep(0.1)
    pyautogui.moveTo(left + move_lelt_a, top + move_top_a)
    time.sleep(0.1)
    pyautogui.dragTo(left + move_lelt_b, top + move_top_b,duration=2,button='left')
    time.sleep(0.1)
    return 0
