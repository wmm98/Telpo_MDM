import Page as public_pack
from Page.Interface_Page import interface

serial = public_pack.Serial()
sub_shell = public_pack.Shell.Shell()
conf = public_pack.Config()
log = public_pack.MyLog()


class AndroidBasePageWiFi(interface):
    def __init__(self, client, times, ip):
        self.client = client
        self.times = times
        self.device_ip = ip

    def get_screen_size(self):
        text = self.u2_send_command("wm size")
        return self.extract_integers(text)

    def swipe_screen(self, x1, y1, x2, y2, duration=0.5):
        self.client.swipe(x1, y1, x2, y2, duration=duration)

    def click_cleat_recent_app_btn(self, id_no):
        # self.click_element(self.get_current_app() + ele)
        # self.u2_send_command(self.get_current_app() + )
        recent_app = self.get_current_app()
        now_time = self.get_current_time()
        while True:
            if self.wait_ele_presence_by_id(recent_app + id_no, 5):
                self.click_element(self.get_element_by_id(recent_app + id_no))
                self.time_sleep(3)
                desktop_app = self.get_current_app()
                if recent_app != desktop_app:
                    return True
            if self.get_current_time() < self.return_end_time(now_time, 60):
                assert False, "@@@@午饭清除最近应用， 请检查！！！！"
            self.time_sleep(1)

    def open_recent_page(self):
        self.back_to_home()
        first_app = self.get_current_app()
        now_time = self.get_current_time()
        while True:
            self.u2_send_command("input keyevent KEYCODE_APP_SWITCH")
            self.time_sleep(2)
            next_app = self.get_current_app()
            if first_app != next_app:
                break
            if self.get_current_time() > self.return_end_time(now_time, 60):
                assert False, "@@@无法打开最近应用页面， 请检查！！！！"

    def open_app_detail_info_page(self, package):
        result = self.u2_send_command(
            "am start -n com.android.settings/.applications.InstalledAppDetails -d package:%s" % package)
        exp = self.remove_space(
            self.upper_transfer("package:%s cmp=com.android.settings/.applications.InstalledAppDetails" % package))
        now_time = self.get_current_time()
        while True:
            if exp in self.remove_space(self.upper_transfer(result)):
                break
            result = self.u2_send_command(
                "am start -n com.android.settings/.applications.InstalledAppDetails -d package:%s" % package)
            if self.get_current_time() > self.return_end_time(now_time):
                assert "@@@@无法打开%s的详细页面， 请检查！！！" % package
            self.time_sleep(3)

    def open_usb_debug_btn(self):
        self.u2_send_command("setprop persist.telpo.debug.mode 1")

    def push_file_to_device(self, orig, des):
        cmd = "push %s %s" % (orig, des)
        # sub_shell.invoke(cmd)
        self.send_adb_command(cmd)
        # self.client.push(orig, des)

    def get_app_userid(self, package):
        id_info = self.u2_send_command("dumpsys package %s | grep userId" % package)
        id_list = self.extract_integers(id_info)
        userid = str(id_list[0])
        return userid

    def screen_off(self):
        self.device_unlock()

    def back_to_home(self):
        self.client.press("home")

    def save_screenshot_to(self, file_path):
        base_path = conf.project_path + "\\ScreenShot\\%s" % file_path
        try:
            self.client.screenshot(base_path)
        except Exception as e:
            self.client.screenshot(base_path)
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

    def confirm_app_is_running(self, package_name, timeout=60):
        self.start_app(package_name)
        self.time_sleep(2)
        now_time = self.get_current_time()
        while True:
            if self.remove_space(package_name) in self.remove_space(self.get_current_app()):
                break
            self.start_app(package_name)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@app没在运行， 请检查！！！！"
            self.time_sleep(2)

    def confirm_app_auto_running(self, package_name, timeout=60):
        now_time = self.get_current_time()
        while True:
            if self.remove_space(package_name) in self.remove_space(self.get_current_app()):
                break
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@app没在运行， 请检查！！！！"
            self.time_sleep(2)

    def reboot_device_multi(self, wlan0_ip):
        self.send_adb_command("reboot")
        self.time_sleep(5)
        self.kill_server()
        self.start_server()
        self.confirm_wifi_adb_connected_multi(wlan0_ip)
        self.device_existed(wlan0_ip)
        # self.confirm_usb_adb_connect(wlan0_ip)
        self.device_boot_complete()
        self.screen_keep_on()

    def reboot_device_root_multi(self, wlan0_ip):
        self.send_adb_command("reboot")
        self.time_sleep(5)
        self.kill_server()
        self.start_server()
        self.confirm_wifi_adb_connected_multi(wlan0_ip)
        self.device_existed(wlan0_ip)
        self.device_boot_complete()
        self.wifi_adb_root(wlan0_ip)
        self.screen_keep_on()

    def reboot_device(self, wlan0_ip):
        self.send_adb_command("reboot")
        self.time_sleep(5)
        self.kill_server()
        self.start_server()
        # self.confirm_wifi_adb_connected(wlan0_ip)
        # self.device_existed(wlan0_ip)
        self.confirm_usb_adb_connect(wlan0_ip)
        self.device_boot_complete()
        # self.wifi_adb_root(wlan0_ip)
        self.screen_keep_on()

    def reboot_device_root(self, wlan0_ip):
        self.send_adb_command("reboot")
        self.time_sleep(5)
        self.kill_server()
        self.start_server()
        # self.confirm_wifi_adb_connected(wlan0_ip)
        # self.device_existed(wlan0_ip)
        self.confirm_usb_adb_connect(wlan0_ip)
        self.device_boot_complete()
        # self.wifi_adb_root(wlan0_ip)
        self.open_root_auth()
        self.screen_keep_on()

    def confirm_usb_adb_connect(self, wlan_ip, timeout=180):
        now_time = self.get_current_time()
        # print(wlan_ip + 'device')
        while True:
            serial.confirm_relay_opened()
            print('%sdevice' % wlan_ip)
            print(":", self.remove_space(self.devices_list()))
            if self.remove_space('%sdevice' % wlan_ip) in self.remove_space(self.devices_list()):
                break
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@USB ADB 无法起来， 请检查！！！"
            self.time_sleep(5)

    def kill_server(self, timeout=120):
        sub_shell.invoke('adb kill-server', runtime=timeout)

    def start_server(self, timeout=120):
        res = sub_shell.invoke('adb start-server', runtime=timeout)
        print(res)

    def wifi_adb_root(self, wlan_ip):
        try:
            self.send_adb_command("root", timeout=5)
        except AssertionError:
            pass
        self.confirm_wifi_adb_connected(wlan_ip)
        self.open_root_auth()

    def device_boot(self, wlan0_ip):
        self.time_sleep(60)
        self.confirm_usb_adb_connect(wlan0_ip)
        # self.confirm_wifi_adb_connected(wlan0_ip)
        self.device_existed(wlan0_ip)
        self.device_boot_complete()
        # self.wifi_adb_root(wlan0_ip)
        self.screen_keep_on()
        # self.device_unlock()

    def device_boot_root(self, wlan0_ip):
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

    def confirm_app_installed(self, apk_path):
        try:
            # self.client.app_install(apk_path)
            package = self.get_apk_package_name(apk_path)
            now_time = self.get_current_time()
            while True:
                if self.app_is_installed(package):
                    break
                self.client.app_install(apk_path)
                if self.get_current_time() > self.return_end_time(now_time):
                    assert False, "@@@@无法安装%s--app, 请检查！！！" % package
                self.time_sleep(3)
        except RuntimeError as e:
            print(e)

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
            self.uninstall_app(package)
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
        file_list = self.get_download_list()
        if len(file_list) != 0:
            for apk in self.get_download_list():
                if "apk" in apk:
                    self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), apk))

    def del_all_content_file(self):
        image_list = [".png", ".jpg", ".webp", "jpeg", ".txt", ".zip"]
        file_list = self.get_download_list()
        if len(file_list) != 0:
            for content in image_list:
                for file in self.get_download_list():
                    if content in file:
                        self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), file))

    def del_file_in_setting_path(self, release_path):
        result = self.u2_send_command("ls /%s/%s" % (self.get_internal_storage_directory(), release_path))
        file_list = result.split("\n")[:-1]
        mage_list = [".txt", ".zip"]
        if len(file_list) != 0:
            for content in mage_list:
                for file in file_list:
                    if content in file:
                        self.rm_file("/%s/%s" % (release_path, file))

    def del_updated_zip(self):
        if "update.zip" in self.u2_send_command("ls /sdcard"):
            print("================存在update文件========================")
            self.rm_file("/%s/%s" % (self.get_internal_storage_directory(), "update.zip"))

    def del_all_downloaded_zip(self):
        file_list = self.get_download_list()
        if len(file_list) != 0:
            for zip_package in self.get_download_list():
                if "zip" in zip_package:
                    self.rm_file("/%s/aimdm/download/%s" % (self.get_internal_storage_directory(), zip_package))

    def download_file_is_existed(self, file_name):
        res = self.u2_send_command(
            "ls /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory(), file_name))
        if self.remove_space(file_name) in self.remove_space(res):
            return True
        else:
            return False

    def get_file_size_in_device(self, file_name):
        "-rw-rw---- 1 root sdcard_rw   73015 2023-09-05 16:51 com.bjw.ComAssistant_1.1.apk"
        res = self.u2_send_command(
            "ls -l /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory(), file_name))
        # get integer list in res
        integer_list = self.extract_integers(res)
        size = int(integer_list[1])
        return size

    def calculate_sha256_in_device(self, file_name):
        # sha256sum sdcard/aimdm/data/2023-10-12.txt
        # 9fb5de71a794b9cb8b8197e6ebfbbc9168176116f7f88aca62b22bbc67c2925a  2023-10-12.txt
        res = self.u2_send_command(
            "ls /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory(), file_name))
        print(res.split("\n")[0])
        download_file_name = res.split("\n")[0]
        cmd = "sha256sum /%s/aimdm/download/%s" % (self.get_internal_storage_directory(), download_file_name)
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

    def is_usb_power(self):
        self.time_sleep(1)
        return self.client.device_info["battery"]["usbPowered"]

    def screen_keep_on(self):
        # self.u2_send_command("settings put system screen_off_timeout 1800000")
        # # self.device_unlock()
        # self.swipe_unlock_screen()
        self.u2_send_command("settings put system screen_off_timeout 1800000")
        # self.device_unlock()
        # self.swipe_unlock_screen()
        self.client.screen_off()
        self.client.press("power")
        self.client.swipe(0.1, 0.9, 0.9, 0.1)
        self.client.swipe(0.1, 0.9, 0.9, 0.1)

    def swipe_unlock_screen(self, battery=True):
        width, height = self.client.window_size()
        self.client.screen_off()
        self.client.screen_on()
        # if battery:
        self.send_shell_command("input swipe %d %d %d %d" % (width/2, height-10, width/2, height-500))

    def device_unlock(self):
        self.device_sleep()
        self.client.unlock()

    def device_sleep(self):
        self.client.screen_off()
        # self.time_sleep(3)
        self.confirm_screen_off()

    def confirm_screen_off(self):
        now_time = self.get_current_time()
        while True:
            result = self.client.info.get("screenOn")
            if not result:
                break
            else:
                self.client.screen_off()
            if self.get_current_time() > self.return_end_time(now_time, 30):
                assert False, "@@@@无法熄屏， 请检查！！！"
            self.time_sleep(1)

    def open_root(self):
        try:
            res = self.send_adb_command("root")
            if len(res) == 0:
                return True
            else:
                return False
        except Exception as e:
            assert False, e

    def open_remount(self):
        try:
            act = self.send_adb_command("remount")
            if "remount succeeded" in act:
                return True
            else:
                return False
        except Exception as e:
            assert False, "@@@remount出错， 请检查！！！"

    def open_root_auth(self):
        act = self.open_root()
        log.info(str(act))
        if not act:
            assert False, "@@@@无法root, 请检查！！！"
        ret = self.open_remount()
        log.info(str(ret))
        if not ret:
            assert False, "@@@@无法remount, 请检查！！！"
        self.time_sleep(5)

    def ping_network_wifi(self, times=5, timeout=120):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = " ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_space("ping: unknown host %s" % "www.baidu.com")
        now_time = self.get_current_time()
        while True:
            print(cmd)
            res = self.remove_space(self.u2_send_command(cmd))
            print(res)
            if exp not in res:
                break
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                if exp in self.remove_space(self.send_shell_command(cmd)):
                    assert False, "@@@@超过2分钟无法上网,请检查网络"
            public_pack.t_time.sleep(2)

    def u2_send_command(self, cmd):
        try:
            return self.client.shell(cmd, timeout=120).output
        except TypeError:
            raise Exception("@@@@传入的指令无效！！！")
        except RuntimeError:
            self.confirm_wifi_adb_connected(self.device_ip, 120)
            return self.client.shell(cmd, timeout=120).output
            # raise Exception("@@@@设备无响应， 查看设备的连接情况！！！")

    def send_shell_command(self, cmd):
        try:
            command = "adb -s %s shell %s" % (self.device_ip, cmd)
            return sub_shell.invoke(command, runtime=30)
        except Exception:
            print("@@@@发送指令超时， 请检查！！！")
            assert False, "@@@@发送指令超时， 请检查！！！"

    def send_adb_command(self, cmd, timeout=30):
        try:
            command = "adb -s %s %s" % (self.device_ip, cmd)
            log.info(command)
            res = sub_shell.invoke(command, runtime=timeout)
            log.info(res)
            return res
        except Exception:
            print("@@@@发送指令超时， 请检查！！！")
            assert False, "@@@@发送指令超时， 请检查！！！"

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

    def press_back(self):
        self.client.press("back")

    def press_enter(self):
        self.client.press("enter")

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

    def ele_text_is_existed(self, text, time_to_wait):
        flag = self.client(text=text).exists(timeout=time_to_wait)
        return flag

    def get_element_by_text(self, text):
        return self.client(text=text)

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
