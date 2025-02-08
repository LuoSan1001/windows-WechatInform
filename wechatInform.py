import time

from flask import Flask, request
from winotify import Notification, Notifier, Registry
import urllib.parse
import win32gui
import win32con

app = Flask(__name__)
notifier = Notifier(Registry(app_id="通知中心", script_path=__file__))

@app.route('/')  # 获取url信息
def getUrlInfo():
    # 完整url
    url = request.url
    # 主机部分
    hostUrl = request.host_url
    # 访问路径
    fullPath = request.full_path
    # 输出
    print('收到推送任务，推送内容是：'+str(urllib.parse.unquote(fullPath.split("/?")[1])).replace('+', ' ', 1))

    # 接收到的内容
    content = str(urllib.parse.unquote(fullPath.split("/?")[1])).replace('+', ' ', 1);

    # 错误处理
    # 因为监听软件那边监听到的首条消息是没有带上微信用户昵称的
    # 所以需要判断当前接收到的消息是不是首条消息
    # 如果不做这一步就会出错

    pdmh = ":" in content
    if pdmh == True:
        # 截取:前面的内容
        qianmian = content.split("》《")[0]
        weixinMsg = content.split("》《")[1]
        print("qianmian: ", qianmian)
        print("weixinmsg: ", weixinMsg)
        # 还要将[]这一块也去掉，这就提取到了微信昵称
        # nickname = qianmian.split("]")[1]
        nickname = qianmian
    else:
        nickname = content.split("》《")[0]
        weixinMsg = content.split("》《")[1]

    # 开发Push通知
    # toaster = ToastNotifier()
    # toaster.show_toast(title=nickname, msg=weixinMsg,icon_path="logo.ico", duration=5)
    notifier.clear()
    time.sleep(0.3)
    toast = notifier.create_notification(title=nickname, msg=weixinMsg, icon=r"D:\WechatInform\wechat.png")
    toast.show()
    return "ok"


def notify(hwnd, msg, wparam, lparam):
    print("notify", msg)
    if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
        print("双击左键", msg)
        pass
    elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
        print("右键弹起", msg)
        pass
    elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
        print("左键弹起", msg)
        pass
    return True

wc = win32gui.WNDCLASS()
wc.hInstance = win32gui.GetModuleHandle(None)
wc.lpszClassName = "微信消息弹窗插件"
wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
wc.lpfnWndProc = notify
classAtom = win32gui.RegisterClass(wc)
hwnd =win32gui.CreateWindow(classAtom,"tst2",win32con.WS_OVERLAPPEDWINDOW,win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,None,None,None,None)
notify_id = (hwnd,0,win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,win32con.WM_USER + 20,win32gui.LoadIcon(0, win32con.IDI_APPLICATION),"Windows通知中心")
win32gui.Shell_NotifyIcon(0,notify_id)

# 在指定IP和端口开启HTTP服务
if __name__ == '__main__':
    app.run(debug=False,host='192.168.0.113', port=8080)