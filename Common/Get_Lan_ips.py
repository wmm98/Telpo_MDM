import threading
from ping3 import ping
import socket


class GetLanIps:
    def __init__(self):
        self.ips_list = []
        self.lock = threading.Lock()

    def ping_ip(self, ip_):
        # 获取线程锁
        try:
            result = ping(ip_, timeout=10)
            if isinstance(result, float):
                # get thread lock
                self.lock.acquire()
                # except local host
                if not self.get_local_ip() == ip_:
                    self.ips_list.append(ip_)
                # print(result1)
                # unlock
                self.lock.release()
        except Exception as e:
            print(e)

    def start_thread(self):
        threads = []
        if self.get_local_ip() != 0:
            base = ".".join((self.get_local_ip().split(".")[:3])) + "."
            ips_list = [base + str(i) for i in range(2, 255)]
            for ip in ips_list:
                t = threading.Thread(target=self.ping_ip, args=(ip,))
                t.start()
                threads.append(t)
            # wait all threads finish
            for thread in threads:
                thread.join()

    def get_local_ip(self):
        try:
            # get local host name
            hostname = socket.gethostname()
            # get local host ip
            host_ip = socket.gethostbyname(hostname)
            return host_ip
        except:
            return 0

    def get_ips_list(self):
        return self.ips_list
