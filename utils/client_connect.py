import utils as public_pack

u2 = public_pack.u2


class ClientConnect:
    def __init__(self):
        pass

    def connect_device(self, addr):
        try:
            global dev
            dev = u2.connect(addr)
            dev.implicitly_wait(10)
            # dev.wait_activity()
        except RuntimeError:
            raise Exception("@@@@设备不在线， 请检查设备与电脑的连接情况！！！！")

    def get_device(self):
        return dev

    def wifi_connect_device(self):
        try:
            global dev_wifi, address
            port = "5555"
            ip_wifi = dev.wlan_ip
            address = ip_wifi + ":" + port
            dev_wifi = u2.connect_adb_wifi(address)
        except Exception as e:
            raise Exception(e)
            # raise Exception("保持电脑和设备在统一局域网下， 请连接同一wifi!!!!")

    def get_wifi_device(self):
        return dev_wifi

    def get_wifi_ip(self):
        return address


if __name__ == '__main__':
    d = ClientConnect()
    d.connect_device("d")
    print(d.get_device())
    d.wifi_connect_device()
    print(d.get_wifi_device())
    # print(d.get_wifi_ip())
