import pyautogui
from Common.Log import MyLog
from easygui import *
from Common import Shell

shell = Shell.Shell()
log = MyLog()


class AlertData:
    def __init__(self):
        pass

    def input_prompt(self):
        global serial
        """:消息输入框  返回值为用户输入的值 点击取消按钮 返回None  点击OK 返回 用户输入的值"""
        ser = pyautogui.prompt(text="请输入当前设备的序列号", title="输入提示框", default="")
        if ser != None:
            serial = ser.replace("\n", "").replace(" ", "").replace("\r", "")
        else:
            serial = 0

    def get_dev_name(self):
        return serial

    def device_serial_client(self, dev):
        global dev_serial
        dev_serial = dev.serial
        # print("这是======device name =========")
        # print(dev_serial)
        # print("这是======device name =========")

    def adb_devices_serial(self):
        return dev_serial

    def getAlert(self, text):
        text = text + "\n " * 10 + " " * 100 + "\n " * 10
        # print(text)
        pyautogui.alert(text=text, title="提示")

    def get_feature_list(self):
        text = "请选择你需要测的模块"
        title = "提示"
        choices = [str(i) for i in range(30)]

        # creating a multi choice box
        output = multchoicebox(text, title, choices)

        # title for the message box
        title = "Message Box"

        # message
        message = "选择的模块为 : " + str(output)

        # creating a message box
        msg = msgbox(message, title)
        msg.callback()
        print(output)

    def get_yes_or_no(self, text):
        while True:
            btnValue = pyautogui.confirm(text=text, title="提示", buttons=['是', '否'])
            if btnValue == None:
                continue
            else:
                if btnValue == '是':
                    return btnValue
                if btnValue == "否":
                    return btnValue


if __name__ == '__main__':
    data = AlertData()
    data.get_feature_list()
