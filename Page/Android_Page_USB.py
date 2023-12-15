import Page as public_pack
from Page.Interface_Page import interface

sub_shell = public_pack.Shell.Shell()
conf = public_pack.Config()
log = public_pack.MyLog()


class AndroidBasePageUSB(interface):
    def __init__(self, client, times, name):
        self.USB_client = client
        self.times = times
        self.device_name = name

    def get_current_wlan(self):
        return self.USB_client.wlan_ip

    def click_cleat_recent_app_btn_USB(self, id_no):
        # self.click_element(self.get_current_app() + ele)
        # self.u2_send_command(self.get_current_app() + )
        recent_app = self.get_current_app_USB()
        now_time = self.get_current_time()
        while True:
            try:
                if self.wait_ele_presence_by_id_USB(recent_app + id_no, 5):
                    self.click_element_USB(self.get_element_by_id_USB(recent_app + id_no))
                    self.time_sleep(3)
                    desktop_app = self.get_current_app_USB()
                    if recent_app != desktop_app:
                        return True
            except AssertionError:
                break
            if self.get_current_time() < self.return_end_time(now_time, 60):
                assert False, "@@@@无法清除最近应用， 请检查！！！！"
            self.time_sleep(1)

    def open_recent_page_USB(self):
        self.back_to_home_USB()
        first_app = self.get_current_app_USB()
        now_time = self.get_current_time()
        while True:
            self.u2_send_command_USB("input keyevent KEYCODE_APP_SWITCH")
            self.time_sleep(2)
            next_app = self.get_current_app_USB()
            if first_app != next_app:
                break
            if self.get_current_time() > self.return_end_time(now_time, 60):
                assert False, "@@@无法打开最近应用页面， 请检查！！！！"

    def open_app_detail_info_page_USB(self, package):
        result = self.u2_send_command_USB("am start -n com.android.settings/.applications.InstalledAppDetails -d package:%s" % package)
        exp = self.remove_space(self.upper_transfer("package:%s cmp=com.android.settings/.applications.InstalledAppDetails" % package))
        now_time = self.get_current_time()
        while True:
            if exp in self.remove_space(self.upper_transfer(result)):
                break
            result = self.u2_send_command_USB("am start -n com.android.settings/.applications.InstalledAppDetails -d package:%s" % package)
            if self.get_current_time() > self.return_end_time(now_time, 60):
                assert False, "@@@@无法打开%s的详细页面， 请检查！！！" % package
            self.time_sleep(3)

    def save_screenshot_to_USB(self, file_path):
        base_path = conf.project_path + "\\ScreenShot\\%s" % file_path
        try:
            self.USB_client.screenshot(base_path)
        except Exception as e:
            self.USB_client.screenshot(base_path)
            print(e)

    def back_to_home_USB(self):
        self.USB_client.press("home")

    def calculate_sha256_in_device_USB(self, file_name):
        # sha256sum sdcard/aimdm/data/2023-10-12.txt
        # 9fb5de71a794b9cb8b8197e6ebfbbc9168176116f7f88aca62b22bbc67c2925a  2023-10-12.txt
        res = self.u2_send_command_USB(
            "ls /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory_USB(), file_name))
        print(res.split("\n")[0])
        download_file_name = res.split("\n")[0]
        cmd = "sha256sum /%s/aimdm/download/%s" % (self.get_internal_storage_directory_USB(), download_file_name)
        print(self.u2_send_command_USB(cmd))
        print(self.u2_send_command_USB(cmd).split(" "))
        result = self.u2_send_command_USB(cmd).split(" ")[0]
        print(result)
        return result

    def start_app_USB(self, package_name):
        self.USB_client.app_start(package_name)
        self.time_sleep(3)
        self.confirm_app_start_USB(package_name)

    def get_current_app_USB(self):
        return self.USB_client.app_current()['package']

    def confirm_app_start_USB(self, package_name):
        now_time = self.get_current_time()
        while True:
            if package_name in self.get_current_app_USB():
                break
            else:
                self.start_app_USB(package_name)
        if self.get_current_time() > self.return_end_time(now_time):
            assert False, "@@@@app无法启动， 请检查！！！！"
        self.time_sleep(2)

    def get_app_info_USB(self, package):
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
            app_information = self.USB_client.app_info(package)
            return app_information
        except public_pack.UiaError as e:
            print("获取app信息发生异常：", e)
            assert False, e

    def get_app_installed_list_USB(self):
        return self.USB_client.app_list()

    def app_is_installed_USB(self, package):
        if package in self.get_app_installed_list_USB():
            return True
        else:
            return False

    def uninstall_app_USB(self, package):
        status = self.USB_client.app_uninstall(package)
        return status

    def get_device_name_USB(self):
        return self.device_name

    def download_file_is_existed_USB(self, file_name):
        res = self.u2_send_command_USB(
            "ls /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory_USB(), file_name))
        if self.remove_space(file_name) in self.remove_space(res):
            return True
        else:
            return False

    def get_file_size_in_device_USB(self, file_name):
        "-rw-rw---- 1 root sdcard_rw   73015 2023-09-05 16:51 com.bjw.ComAssistant_1.1.apk"
        res = self.u2_send_command_USB(
            "ls -l /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory_USB(), file_name))
        # get integer list in res
        integer_list = self.extract_integers(res)
        size = int(integer_list[1])
        return size

    def get_internal_storage_directory_USB(self):
        if "aimdm" in self.u2_send_command_USB("ls sdcard/"):
            return "sdcard"
        elif "aimdm" in self.u2_send_command_USB("ls data/"):
            return "data"
        else:
            assert False, "@@@@ 内部sdcard和data下均不存在aimdm文件夹， 请检查设备内核版本！！！！"

    def get_cur_wifi_status(self):
        return self.u2_send_command_USB("settings get global wifi_on")

    def wifi_open_status(self):
        return self.text_is_existed("1", self.get_cur_wifi_status())

    def wifi_close_status(self):
        return self.text_is_existed("0", self.get_cur_wifi_status())

    def open_wifi_btn(self):
        if "0" in self.get_cur_wifi_status():
            self.u2_send_command_USB("svc wifi enable")
            return self.wifi_open_status()
        return True

    def close_wifi_btn(self):
        if "1" in self.get_cur_wifi_status():
            self.u2_send_command_USB("svc wifi disable")
            return self.wifi_close_status()
        else:
            return True

    def confirm_wifi_status_open(self, timeout=120):
        now_time = self.get_current_time()
        while True:
            if self.wifi_open_status():
                break
            self.open_wifi_btn()
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@超过2分钟打开wifi按钮， 请检查！！！"
            self.time_sleep(3)

    def confirm_wifi_status_close(self, timeout=120):
        now_time = self.get_current_time()
        while True:
            if self.wifi_close_status():
                break
            self.close_wifi_btn()
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@超过2分钟关闭wifi按钮， 请检查！！！"
            self.time_sleep(3)

    def ping_network(self, times=5, timeout=120):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = " ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_space("ping: unknown host %s" % "www.baidu.com")
        now_time = self.get_current_time()
        while True:
            print(cmd)
            res = self.remove_space(self.u2_send_command_USB(cmd))
            print(res)
            if exp not in res:
                return True
            if self.get_current_time() > self.return_end_time(now_time, timeout=timeout):
                # if exp in self.remove_space(self.send_shell_command_USB(cmd)):
                assert False, "@@@@超过%d s无法上网,请检查网络" % timeout
            public_pack.t_time.sleep(2)

    def no_network(self, times=5, timeout=30):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = "ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_space("ping: unknown host %s" % "www.baidu.com")
        now_time = self.get_current_time()
        while True:
            print(cmd)
            res = self.remove_space(self.u2_send_command_USB(cmd))
            print(res)
            if exp in res:
                return True
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                if exp in self.remove_space(self.send_shell_command_USB(cmd)):
                    assert False, "@@@@网络还没有关闭， 请检查！！！！"
            public_pack.t_time.sleep(2)

    def screen_keep_on_USB(self):
        self.u2_send_command_USB("settings put system screen_off_timeout 1800000")
        self.swipe_unlock_screen_USB()

    def swipe_unlock_screen_USB(self, battery=True):
        width, height = self.USB_client.window_size()
        self.USB_client.screen_off()
        self.USB_client.screen_on()
        # if battery:
        self.send_shell_command_USB("input swipe %d %d %d %d" % (width/2, height-100, width/2, height-500))

    def device_unlock_USB(self):
        self.USB_client.screen_off()
        self.USB_client.unlock()

    def confirm_screen_off_USB(self):
        now_time = self.get_current_time()
        while True:
            result = self.USB_client.info.get("screenOn")
            if not result:
                break
            else:
                self.USB_client.screen_off()
            if self.get_current_time() > self.return_end_time(now_time, 30):
                assert False, "@@@@无法熄屏， 请检查！！！"
            self.time_sleep(1)

    def u2_send_command_USB(self, cmd):
        try:
            print(cmd)
            res = self.USB_client.shell(cmd, timeout=120).output
            print(res)
            return res
        except Exception as e:
            print(e)
        # except TypeError:
        #     raise Exception("@@@@传入的指令无效！！！")
        # except RuntimeError:
        #     raise Exception("@@@@设备无响应， 查看设备的连接情况！！！")

    def send_shell_command_USB(self, cmd):
        try:
            command = "adb -s %s shell %s" % (self.device_name, cmd)
            return sub_shell.invoke(command, runtime=30)
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def send_adb_command_USB(self, cmd, timeout=30):
        try:
            command = "adb -s %s %s" % (self.device_name, cmd)
            print("command:", command)
            res = sub_shell.invoke(command, runtime=timeout)
            return res
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def device_boot_complete_USB(self):
        time_out = self.get_current_time() + 120
        try:
            while True:
                boot_res = self.send_shell_command_USB("getprop sys.boot_completed")
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
                boot_res = self.send_shell_command_USB("getprop sys.boot_completed")
                print(boot_res)
                if str(1) in boot_res:
                    break
                self.time_sleep(2)
        except Exception as e:
            assert False, "@@@@启动出问题，请检查设备启动情况！！！"

    def click_element_USB(self, ele):
        ele.click()

    def get_element_text_USB(self, ele):
        text = ele.get_text()
        return text

    def input_element_text_USB(self, ele, text):
        ele.clear_text()
        ele.send_keys(text)

    def get_element_by_id_USB(self, id_no, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        if self.wait_ele_presence_by_id_USB(id_no, time_to_wait):
            return self.USB_client(resourceId=id_no)

    def get_element_by_id_no_wait_USB(self, id_no):
        return self.USB_client(resourceId=id_no)

    def get_element_by_class_name_USB(self, class_name, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        self.wait_ele_presence_by_class_name_USB(class_name, time_to_wait)
        return self.USB_client(className=class_name)

    def wait_ele_presence_by_id_USB(self, id_no, time_to_wait):
        flag = self.USB_client(resourceId=id_no).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def ele_id_is_existed_USB(self, loc, timeout=5):
        return self.USB_client(resourceId=loc).exists(timeout=timeout)

    def confirm_ele_is_existed_USB(self, pre_ele, loc):
        now_time = self.get_current_time()
        while True:
            if self.ele_id_is_existed_USB(loc):
                break
            pre_ele.click()
            self.time_sleep(1)
            if self.get_current_time() > self.return_end_time(now_time, 120):
                btn_text = self.get_element_text_USB(pre_ele)
                assert False, "@@@@点击按钮%s不生效, 请检查！！！" % btn_text

    def wait_ele_presence_by_class_name_USB(self, class_name, time_to_wait):
        flag = self.USB_client(className=class_name).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_gone_by_id_USB(self, id_no, wait):
        if wait == 0:
            time_to_wait = 5
        else:
            time_to_wait = wait
        return self.USB_client(resourceId=id_no).wait_gone(timeout=time_to_wait)

    def wait_ele_gone_by_class_name_USB(self, class_name, time_to_wait):
        return self.USB_client(className=class_name).exists(timeout=time_to_wait)

    def alert_show(self, id_no, time_to_wait):
        try:
            self.wait_ele_presence_by_id_USB(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def alert_fade(self, id_no, time_to_wait):
        try:
            self.wait_ele_gone_by_id_USB(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def wait_alert_fade_USB(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_fade(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)

    def wait_alert_appear_USB(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_show(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)

    def open_mobile_data(self):
        cmd = "svc data enable"
        print(cmd)
        result = self.u2_send_command_USB(cmd)
        print(result)
        self.u2_send_command_USB(cmd)
        self.time_sleep(3)

    def close_mobile_data(self):
        cmd = "svc data disable"
        print(cmd)
        result = self.u2_send_command_USB(cmd)
        print(result)
        # res1 = self.u2_send_command_USB(cmd)

    def open_root_usb(self):
        try:
            res = self.send_adb_command_USB("root")
            if len(res) == 0:
                return True
            else:
                return False
        except Exception as e:
            assert False, e

    def open_remount_usb(self):
        try:
            act = self.send_adb_command_USB("remount")
            if "remount succeeded" in act:
                return True
            else:
                return False
        except Exception as e:
            assert False, "@@@remount出错， 请检查！！！"

    def open_root_auth_usb(self):
        if 'Qualcomm' in self.get_device_info()['cpu']['hardware']:
            if self.get_device_info()['model'] in ['T20', 'T10']:
                act = self.open_root_usb()
                if not act:
                    assert False, "@@@@无法root, 请检查！！！"
                self.time_sleep(3)
                ret = self.open_remount_usb()
                if not ret:
                    assert False, "@@@@无法remount, 请检查！！！"
                self.time_sleep(3)

                act1 = self.open_root_usb()
                if not act1:
                    assert False, "@@@@无法root, 请检查！！！"
                self.time_sleep(3)
                ret1 = self.open_remount_usb()
                if not ret1:
                    assert False, "@@@@无法remount, 请检查！！！"
                self.time_sleep(3)
        else:
            act = self.open_root_usb()
            if not act:
                assert False, "@@@@无法root, 请检查！！！"
            # ret = self.open_remount_usb()
            # if not ret:
            #     assert False, "@@@@无法remount, 请检查！！！"
            self.time_sleep(3)

    def get_device_info(self):
        info = self.USB_client.device_info
        return info


if __name__ == '__main__':
    from utils.client_connect import ClientConnect

    conn = ClientConnect()
    conn.connect_device("d")
    d = conn.get_device()
    page = AndroidBasePageUSB(d, 10, d.serial)
    res = page.u2_send_command_USB("getprop ro.serialno")
    print(res)
    element = page.get_element_by_id_USB("com.tpos.aimdm:id/tip")
    print(page.get_element_text_USB(element))
    # if ele:
    #     print(page.get_element_text(ele))
