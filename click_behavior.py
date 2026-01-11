import time
import math
import cv2
import pyautogui

import pywinctl as pwc

def get_xy(img_model_path):
    """
    找到需要点击什么的坐标
    :param img_model_path:输入需要找的图片
    :return:坐标,匹配度（1是完全，0是不匹配）
    """
    #截图

    pyautogui.screenshot().save("./screenshot/123.png")

    #载入截图
    img = cv2.imread("./screenshot/123.png")

    #要找的模板
    img_terminal = cv2.imread(img_model_path)

    #读取模板宽度和高度
    height,width,ch= img_terminal.shape

    #匹配，返回一个值
    result=cv2.matchTemplate(img,img_terminal, cv2.TM_SQDIFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 匹配率查看（TM_SQDIFF_NORMED越接近0越匹配,所以这里反一下）
    match_rate = math.sqrt(min_val)
    # match_rate = min_val
    print(f"匹配率: {1-match_rate:.4f}")

    #这个输出的是左上角坐标，是result的第3个值
    upper_left = cv2.minMaxLoc(result)[2]


    #算出右下角，这里要注意，你不能直接取出右下角，不然会发生不幸。截图需要准确
    lower_right = (upper_left[0]+ width, upper_left[1]+height)

    #计算中心
    avg= (int((upper_left[0]+lower_right[0])/2),int((upper_left[1]+lower_right[1])/2))
    return avg,1-match_rate

def click_auto (var_avg):
    """
    接受要点的坐标然后点
    :param var_avg:坐标组
    :return:不
    """
    #这里采取的先移动后点击的策略，如果直接点击，游戏会判定无效
    pyautogui.moveTo(var_avg[0],var_avg[1])
    time.sleep(0.1) #等待一会
    pyautogui.click(var_avg[0],var_avg[1],button='left')

    print('当前点击事件执行')

    #点击完成等待0.5秒，防止奇怪的问题发生
    time.sleep(0.1)


def routine (img_model_path,name):
    """
    点击的事实上的使用函数
    :param img_model_path:图片
    :param name:这个没有实际作用，只是一个提示
    :return:输出2代表点了，输出1代表没点
    """
    avg,match_rate= get_xy(img_model_path)

    if match_rate>0.8:
        print(f'点击{name}')
        click_auto(avg)
        return int(2)
    else:
        print(f'匹配率太低，不点击{name}')
        return int(1)


def routine_only_find (img_model_path,name):
    """
    点击的事实上的使用函数
    :param img_model_path:图片
    :param name:这个没有实际作用，只是一个提示
    :return:输出2代表点了，输出1代表没点
    """
    avg,match_rate= get_xy(img_model_path)

    if match_rate>0.8:
        print(f'存在{name}元素，不会点击')
        # click_auto(avg)
        return int(2)
    else:
        print(f'匹配率太低，不存在{name}元素，这个不会进行点击')
        return int(1)

def find_win(title):
    """
    点击的事实上的使用函数
    :param img_model_path:图片
    :param name:这个没有实际作用，只是一个提示
    :return:输出2代表点了，输出1代表没点
    """

    wins = pwc.getWindowsWithTitle(title)
    if not wins:
        print(f"找不到窗口: {title}\n")
        return int(2)

    w = wins[0]
    if w.isMinimized:
        w.restore()
        print(f"正常找到\n")
    w.activate()  # 置前/聚焦
    print(f"窗口已弹出\n")
    time.sleep(0.2)
    print(f"返回的两个数据是，left：{w.left}，top：{w.top}")
    return w.left,w.top#这个参数第一个越大越右边，第二个越大越往下




#routine("./aim/2222.png",'bbb')