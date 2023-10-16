import Page as public_pack
from Page.Interface_Page import interface

sub_shell = public_pack.Shell.Shell()
conf = public_pack.Config()


class AndroidBasePageWiFi(interface):
    def __init__(self, client, times, ip):
        self.client = client
        self.times = times
        self.device_ip = ip

    def save_screenshot_to(self, file_path):
        base_path = conf.project_path + "\\ScreenShot\\%s" % file_path
        try:
            self.client.screenshot(base_path)
        except Exception as e:
            print(e)

    def stop_app(self, package_name):
        self.client.app_stop(package_name)
        self.confirm_app_stop(package_name)

    def confirm_app_stop(self, package_name):
        now_time = self.get_current_time()
        while True:
            if package_name not in self.get_current_app():
                break
            else:
                self.stop_app(package_name)
        if self.get_current_time() > self.return_end_time(now_time):
            assert False, "@@@@app无法启动， 请检查！！！！"
        self.time_sleep(2)

    def start_app(self, package_name):
        self.client.app_start(package_name)
        self.time_sleep(3)
        self.confirm_app_start(package_name)

    def get_current_app(self):
        res = self.client.app_current()['package']
        print(res)
        return res

    def confirm_app_start(self, package_name):
        now_time = self.get_current_time()
        while True:
            if package_name in self.get_current_app():
                break
            else:
                self.start_app(package_name)
        if self.get_current_time() > self.return_end_time(now_time):
            assert False, "@@@@app无法启动， 请检查！！！！"
        self.time_sleep(2)

    def confirm_app_is_running(self, package_name):
        now_time = self.get_current_time()
        while True:
            if self.remove_space(package_name) in self.remove_space(self.get_current_app()):
                break
        if self.get_current_time() > self.return_end_time(now_time, 60):
            assert False, "@@@@app没在运行， 请检查！！！！"
        self.time_sleep(2)

    def reboot_device(self, wlan0_ip):
        self.send_adb_command("reboot")
        self.time_sleep(5)
        self.confirm_wifi_adb_connected(wlan0_ip)
        self.device_existed(wlan0_ip)
        self.device_boot_complete()
        self.device_unlock()

    def device_boot(self, wlan0_ip):
        self.time_sleep(5)
        self.confirm_wifi_adb_connected(wlan0_ip)
        self.device_existed(wlan0_ip)
        self.device_boot_complete()
        self.device_unlock()

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

    def uninstall_app_post(self, apk_name):
        file_path = self.get_apk_path(apk_name)
        if public_pack.os.path.exists(file_path):
            package = self.get_apk_package_name(file_path)
            status = self.client.app_uninstall(package)
            return status

    def uninstall_multi_apps(self, apps_dict):
        for app_key in apps_dict:
            file_path = self.get_apk_path(apps_dict[app_key])
            package = self.get_apk_package_name(file_path)
            self.uninstall_app(package)

    def confirm_app_is_uninstalled(self, package):
        self.uninstall_app(package)
        now_time = self.get_current_time()
        while True:
            if not self.app_is_installed(package):
                break
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@无法卸载%s--app, 请检查！！！" % package
            self.time_sleep(3)

    def get_device_name(self):
        return self.device_ip

    def get_download_list(self):
        res = self.u2_send_command("ls /%s/aimdm/download/" % self.get_internal_storage_directory())
        files = res.split("\n")[:-1]
        return files

    def rm_file(self, file_name):
        self.u2_send_command("rm %s" % file_name)

    def del_all_downloaded_apk(self):
        print("ls /%s/aimdm/download" % self.get_internal_storage_directory())
        print(self.u2_send_command("ls /%s/aimdm/download" % self.get_internal_storage_directory()))
        try:
            for apk in self.get_download_list():
                self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), apk))
        except Exception as e:
            print(e)
            file_list = self.get_download_list()
            if len(file_list) != 0:
                for apk in self.get_download_list():
                    if "apk" in apk:
                        self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), apk))
        print("ls /%s/aimdm/download" % self.get_internal_storage_directory())
        print(self.u2_send_command("ls /%s/aimdm/download" % self.get_internal_storage_directory()))

    def del_updated_zip(self):
        try:
            print(self.u2_send_command("ls /sdcard"))
            if "update.zip" in self.u2_send_command("ls /sdcard"):
                print("================存在update文件========================")
                self.rm_file("/%s/%s" % (self.get_internal_storage_directory(), "update.zip"))
        except Exception as e:
            print(e)
            file_list = self.get_download_list()
            if len(file_list) != 0:
                for apk in self.get_download_list():
                    if "apk" in apk:
                        self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), apk))

    def del_all_downloaded_zip(self):
        try:
            for zip_package in self.get_download_list():
                self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), zip_package))
        except Exception as e:
            print(e)
            file_list = self.get_download_list()
            if len(file_list) != 0:
                for zip_package in self.get_download_list():
                    if "zip" in zip_package:
                        self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), zip_package))

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

    def calculate_sha256_in_device(self, file_name):
        # sha256sum sdcard/aimdm/data/2023-10-12.txt
        # 9fb5de71a794b9cb8b8197e6ebfbbc9168176116f7f88aca62b22bbc67c2925a  2023-10-12.txt
        cmd = "sha256sum /%s/aimdm/download/%s" % (self.get_internal_storage_directory(), file_name)
        print(self.u2_send_command(cmd))
        print(self.u2_send_command(cmd).split(" "))
        result = self.u2_send_command(cmd).split(" ")[0]
        print(result)
        return result

    def get_internal_storage_directory(self):
        if "aimdm" in self.u2_send_command("ls sdcard/"):
            return "sdcard"
        elif "aimdm" in self.u2_send_command("ls data/"):
            return "data"
        else:
            assert False, "@@@@ 内部sdcard和data下均不存在aimdm文件夹， 请检查设备内核版本！！！！"

    def text_is_existed(self, text1, text2):
        sub = self.remove_space(text1)
        string = self.remove_space(text2)
        if sub in string:
            return True
        else:
            return True

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
            command = "adb -s %s shell %s" % (self.device_ip, cmd)
            return sub_shell.invoke(command, runtime=30)
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def send_adb_command(self, cmd):
        try:
            command = "adb -s %s %s" % (self.device_ip, cmd)
            res = sub_shell.invoke(command, runtime=30)
            return res
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def device_boot_complete(self):
        time_out = self.get_current_time() + 60
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
            assert False, "@@@@正常开机后出问题，完全启动超过60s, 请检查！！！！！！！"

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

    def click_element(self, ele1):
        ele1.click()

    def get_element_text(self, ele):
        text = ele.get_text()
        return text

    def input_element_text(self, ele, text):
        ele.clear_text()
        ele.send_keys(text)

    def get_element_by_id(self, id_no, timeout=5):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        if self.wait_ele_presence_by_id(id_no, time_to_wait):
            return self.client(resourceId=id_no)

    def get_element_by_id_no_wait(self, id_no):
        return self.client(resourceId=id_no)

    def get_element_by_class_name(self, class_name, timeout=5):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        self.wait_ele_presence_by_class_name(class_name, time_to_wait)
        return self.client(className=class_name)

    def wait_ele_presence_by_id(self, id_no, time_to_wait):
        flag = self.client(resourceId=id_no).exists(timeout=time_to_wait)
        return flag
        # if flag:
        #     return True
        # else:
        #     assert False, "@@@@查找元素超时！！！"

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

    def get_device_sn(self):
        return self.remove_space(str(self.u2_send_command("getprop ro.serialno")))


if __name__ == '__main__':
    from utils.client_connect import ClientConnect

    conn = ClientConnect()
    conn.connect_device("d")
    d = conn.get_device()
    page = AndroidBasePageWiFi(d, 10, d.serial)
    res = page.u2_send_command("getprop ro.serialno")
    print(res)
    element = page.get_element_by_id("com.tpos.aimdm:id/tip")
    print(page.get_element_text(element))
    # if ele:
    #     print(page.get_element_text(ele))
