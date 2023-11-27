import binascii
import serial
import time
from Common.Log import MyLog
import serial.tools.list_ports
from Common import DealAlert

alert = DealAlert.AlertData()

log = MyLog()


class Serial:
    def __init__(self):
        self.COM = ''

    def get_cur_COM(self):
        serial_list = []
        ports = list(serial.tools.list_ports.comports())
        # print(ports)
        if len(ports) != 0:
            for port in ports:
                if 'SERIAL' in port.description:
                    print(port.device)
                    COM_name = port.device.replace("\n", "").replace(" ", "").replace("\r", "")
                    serial_list.append(COM_name)
            if len(serial_list) == 1:
                self.COM = serial_list[0]
            else:
                text = alert.get_alert_value("当前多个可用串口，请输入自动化用的端口号")
                self.COM = text
        else:
            raise Exception("没有显示可用的串口端口， 请检查！！！！")

    def logoutSer(self):
        if ser.isOpen():
            ser.close()
            log.info("串口： %s 关闭！！！" % self.COM)
        else:
            log.info("串口： %s 关闭！！！" % self.COM)

    # 打开串口
    def loginSer(self):
        global ser
        port = self.COM  # 设置端口号
        baudrate = 9600  # 设置波特率
        bytesize = 8  # 设置数据位
        stopbits = 1  # 设置停止位
        parity = "N"  # 设置校验位

        try:
            ser = serial.Serial(port, baudrate)
        except serial.SerialException as e:
            print(e)
        if (ser.isOpen()):  # 判断串口是否打开
            log.info("串口：%s 已经打开！！！" % self.COM)
        else:
            ser.open()
            log.info("串口：%s 打开！！！" % self.COM)

    def send_ser_connect_cmd(self, conn=True):
        if conn:
            ser.write(bytes.fromhex("A0 01 01 A2"))
        else:
            ser.write(bytes.fromhex("A0 01 00 A1"))
        time.sleep(1)

    def send_status_cmd(self):
        num = ser.write(bytes.fromhex("A0 01 05 A6"))
        time.sleep(2)  # sleep() 与 inWaiting() 最好配对使用
        ser.inWaiting()

        data = str(binascii.b2a_hex(ser.read(num)))[2:-1]  # 十六进制显示方法2
        print(data)
        if "a00100a1" in data:
            return False
        elif "a00101a2" in data:
            return True

    def confirm_relay_opened(self, timeout=120):
        now_time = time.time()
        while True:
            self.send_ser_connect_cmd(conn=True)
            if self.send_status_cmd():
                log.info("成功打开继电器")
                break
            time.sleep(1)
            if time.time() > now_time + timeout:
                log.error("@@@@无法打开继电器，请检查！！！！")
                assert False, "@@@@无法打开继电器，请检查！！！！"

    def confirm_relay_closed(self, timeout=120):
        now_time = time.time()
        while True:
            self.send_ser_connect_cmd(conn=False)
            if not self.send_status_cmd():
                log.info("成功关闭继电器")
                break
            time.sleep(1)
            if time.time() > now_time + timeout:
                log.error("@@@@无法打开继电器，请检查！！！！")
                assert False, "@@@@无法打开继电器，请检查！！！！"


if __name__ == '__main__':
    s = Serial()
    s.get_cur_COM()
    s.loginSer()
    s.confirm_relay_opened()
    s.confirm_relay_closed()
    s.logoutSer()


