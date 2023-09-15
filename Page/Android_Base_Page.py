import Page as public_pack
from Page.Interface_Page import interface

sub_shell = public_pack.Shell.Shell()


class AndroidBasePage(interface):
    def __init__(self, client, times, name):
        self.client = client
        self.times = times
        self.device_name = name

    def get_app_info(self, package):
        """
        Return example:
            {
                "mainActivity": "com.github.uiautomator.MainActivity",
                "label": "ATX",
                "versionName": "1.1.7",
                "versionCode": 1001007,
                "size":1760809
            }
            """
        try:
            app_information = self.client.app_info(package)
            return app_information
        except public_pack.UiaError as e:
            print("获取app信息发生异常：", e)
            assert False, e

    def get_app_installed_list(self):
        return self.client.app_list()

    def app_is_installed(self, package):
        if package in self.get_app_installed_list():
            return True
        else:
            return False

    def uninstall_app(self, package):
        status = self.client.app_uninstall(package)
        return status

    def get_device_name(self):
        return self.device_name

    def download_file_is_existed(self, file_name):
        res = self.u2_send_command("ls /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory(), file_name))
        if self.remove_space(file_name) in self.remove_space(res):
            return True
        else:
            return False

    def get_file_size_in_device(self, file_name):
        "-rw-rw---- 1 root sdcard_rw   73015 2023-09-05 16:51 com.bjw.ComAssistant_1.1.apk"
        res = self.u2_send_command("ls -l /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory(), file_name))
        # get integer list in res
        integer_list = self.extract_integers(res)
        size = int(integer_list[1])
        return size

    def get_internal_storage_directory(self):
        if "aimdm" in self.u2_send_command("ls sdcard/"):
            return "sdcard"
        elif "aimdm" in self.u2_send_command("ls data/"):
            return "data"
        else:
            assert False, "@@@@ 内部sdcard和data下均不存在aimdm文件夹， 请检查设备内核版本！！！！"

    def get_cur_wifi_status(self):
        return self.u2_send_command("settings get global wifi_on")

    def wifi_open_status(self):
        return self.text_is_existed("1", self.get_cur_wifi_status())

    def wifi_close_status(self):
        return self.text_is_existed("0", self.get_cur_wifi_status())

    def open_wifi_btn(self):
        if "0" in self.get_cur_wifi_status():
            self.u2_send_command("svc wifi enable")
            return self.wifi_open_status()
        return True

    def close_wifi_btn(self):
        if "1" in self.get_cur_wifi_status():
            self.u2_send_command("svc wifi disable")
            return self.wifi_close_status()
        return True

    def text_is_existed(self, text1, text2):
        sub = self.remove_space(text1)
        string = self.remove_space(text2)
        if sub in string:
            return True
        else:
            return True

    def ping_network(self, times, timeout=120):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = " ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_space("ping: unknown host %s" % "www.baidu.com")
        now_time = self.get_current_time()
        while True:
            res = self.remove_space(self.send_shell_command(cmd))
            print(res)
            if exp not in res:
                return True
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                if exp in self.remove_space(self.send_shell_command(cmd)):
                    assert False, "@@@@超过2分钟无法上网,请检查网络"
            public_pack.t_time.sleep(2)

    def device_unlock(self):
        self.client.screen_off()
        self.client.unlock()

    def u2_send_command(self, cmd):
        try:
            return self.client.shell(cmd, timeout=120).output
        except TypeError:
            raise Exception("@@@@传入的指令无效！！！")
        except RuntimeError:
            raise Exception("@@@@设备无响应， 查看设备的连接情况！！！")

    def send_shell_command(self, cmd):
        try:
            command = "adb -s %s shell %s" % (self.device_name, cmd)
            return sub_shell.invoke(command, runtime=30)
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def send_adb_command(self, cmd):
        try:
            command = "adb -s %s %s" % (self.device_name, cmd)
            res = sub_shell.invoke(command, runtime=30)
            return res
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def device_boot_complete(self):
        time_out = self.get_current_time() + 120
        try:
            while True:
                boot_res = self.send_shell_command("getprop sys.boot_completed")
                print(boot_res)
                if str(1) in boot_res:
                    break
                if self.get_current_time() > time_out:
                    print("完全启动超时")
                self.time_sleep(2)
        except Exception as e:
            assert False, "@@@@启动出问题，请检查设备启动情况！！！"

    def device_boot_complete_debug_off(self):
        try:
            while True:
                boot_res = self.send_shell_command("getprop sys.boot_completed")
                print(boot_res)
                if str(1) in boot_res:
                    break
                self.time_sleep(2)
        except Exception as e:
            assert False, "@@@@启动出问题，请检查设备启动情况！！！"

    def devices_list(self):
        return sub_shell.invoke("adb devices")

    def device_exist(self):
        while True:
            res = sub_shell.invoke("adb devices")
            print(res)
            if self.device_name in res.replace('\r', '').replace('\t', '').replace(' ', ''):
                break
            self.time_sleep(2)

    def click_element(self, ele):
        ele.click()

    def get_element_text(self, ele):
        text = ele.get_text()
        return text

    def input_element_text(self, ele, text):
        ele.clear_text()
        ele.send_keys(text)

    def get_element_by_id(self, id_no, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        if self.wait_ele_presence_by_id(id_no, time_to_wait):
            return self.client(resourceId=id_no)

    def get_element_by_id_no_wait(self, id_no):
        return self.client(resourceId=id_no)

    def get_element_by_class_name(self, class_name, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        self.wait_ele_presence_by_class_name(class_name, time_to_wait)
        return self.client(className=class_name)

    def wait_ele_presence_by_id(self, id_no, time_to_wait):
        flag = self.client(resourceId=id_no).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_presence_by_class_name(self, class_name, time_to_wait):
        flag = self.client(className=class_name).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_gone_by_id(self, id_no, wait):
        if wait == 0:
            time_to_wait = 5
        else:
            time_to_wait = wait
        return self.client(resourceId=id_no).wait_gone(timeout=time_to_wait)

    def wait_ele_gone_by_class_name(self, class_name, time_to_wait):
        return self.client(className=class_name).exists(timeout=time_to_wait)

    def alert_show(self, id_no, time_to_wait):
        try:
            self.wait_ele_presence_by_id(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def alert_fade(self, id_no, time_to_wait):
        try:
            self.wait_ele_gone_by_id(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def wait_alert_fade(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_fade(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)

    def wait_alert_appear(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_show(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)


if __name__ == '__main__':
    from utils.client_connect import ClientConnect

    conn = ClientConnect()
    conn.connect_device("d")
    d = conn.get_device()
    page = AndroidBasePage(d, 10, d.serial)
    res = page.u2_send_command("getprop ro.serialno")
    print(res)
    element = page.get_element_by_id("com.tpos.aimdm:id/tip")
    print(page.get_element_text(element))
    # if ele:
    #     print(page.get_element_text(ele))
