import binascii
import serial
import time


class Serial:
    def __init__(self):
        self.COM = 'COM24'

    def logoutSer(self):
        if (ser.isOpen()):
            ser.close()
            print("关闭成功")
            print('The serial %s is closed!' % self.COM)
        else:
            print("关闭失败")
            print('The serial %s is not closed!' % self.COM)

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
            print('串口打开成功')
            # self.log.info('The serial %s is open!' % self.config.serialcom)
            # print('The serial %s is open!' % self.COM)
        else:
            ser.open()
            print('串口打开成功!!')
            # print('The serial %s is open!' % self.COM)

    def send_ser_cmd(self, conn=True):
        if conn:
            n = ser.write(bytes.fromhex("A0 01 01 A2"))
        else:
            n = ser.write(bytes.fromhex("A0 01 00 A1"))

        print(n)
        time.sleep(2)  # sleep() 与 inWaiting() 最好配对使用
        num = ser.inWaiting()
        print("接受的数据：", num)
        # 接受数据
        # if num:
        #     try:  # 如果读取的不是十六进制数据--
        #         data = str(binascii.b2a_hex(ser.read(num)))[2:-1]  # 十六进制显示方法2
        #     except:  # -则将其作为字符串读取
        #         str = ser.read(num)
        #         return self.hexShow(str)


if __name__ == '__main__':
    s = Serial()
    #
    s.loginSer()
    s.send_ser_cmd(conn=True)
    s.logoutSer()

    # assert s.ast.assertSingleLEDStatus(result,3,checkdata)
    # command = 'A0 01 01 A2'
    # result = s.inputSerCommand(command)
    # print(result)

    # import serial
    #
    # # 串口的端口和波特率
    # port = "COM24"
    # baudrate = 9600
    #
    # # 建立串口连接
    # ser = serial.Serial(port, baudrate)
    # # A0 01 01 A2  打开  A0 01 00 A1  关闭
    # # 待发送的指令
    # command = bytes.fromhex("A0 01 00 A1")
    #
    # # 发送指令
    # ser.write(command)
    #
    # # 关闭串口连接
    # ser.close()
