import utils as public_pack

u2 = public_pack.u2


class ClientConnect:
    def __init__(self):
        pass

    def connect_device(self, address):
        try:
            global dev
            dev = u2.connect(address)
            dev.implicitly_wait(10)
            # dev.wait_activity()
        except RuntimeError:
            raise Exception("@@@@设备不在线， 请检查设备与电脑的连接情况！！！！")

    def get_device(self):
        return dev


if __name__ == '__main__':
    d = ClientConnect()
    d.connect_device("d")
    d.get_device()
