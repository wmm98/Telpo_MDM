import Page as public_pack
from Page.Android_Page_USB import AndroidBasePageUSB
from Page.Android_Page_WiFi import AndroidBasePageWiFi
import time

config = public_pack.Config()


class AndroidAimdmPage(AndroidBasePageUSB, AndroidBasePageWiFi):
    def __init__(self, devices_data, times):
        self.client = devices_data["usb_device_info"]["device"]
        self.serial = devices_data["usb_device_info"]["serial"]
        self.wifi_client = devices_data["wifi_device_info"]["device"]
        self.device_ip = devices_data["wifi_device_info"]["ip"]
        AndroidBasePageUSB.__init__(self, self.client, times, self.serial)
        AndroidBasePageWiFi.__init__(self, self.wifi_client, times, self.device_ip)

    aimdm_package = "com.tpos.aimdm"
    # msg_box related
    msg_header_id = "android.widget.TextView"
    msg_tips_id = "%s:id/tip" % aimdm_package
    msg_confirm_id = "%s:id/confirm" % aimdm_package
    msg_cancel_id = "%s:id/cancel" % aimdm_package
    msg_alert_id = "%s:id/root_view" % aimdm_package
    # 900P  confirm->download->confirm->upgrade

    # lock alert, input device psw relate
    lock_psw_id = "%s:id/et_pwd" % aimdm_package
    psw_confirm_id = "%s:id/confirm_pwd" % aimdm_package

    def check_firmware_version(self):
        return self.u2_send_command("getprop ro.product.version")

    def confirm_received_alert(self, exp_tips):
        # self.mdm_msg_alert_show()
        self.confirm_alert_show()
        self.confirm_received_text(exp_tips)
        self.click_msg_confirm_btn()
        self.confirm_msg_alert_fade(exp_tips)

    def confirm_received_text(self, exp):
        now_time = self.get_current_time()
        while True:
            exp_text = self.upper_transfer(self.remove_space(exp))
            act_text = self.upper_transfer(self.remove_space(self.get_msg_tips_text()))
            if exp_text == act_text:
                break
            if self.get_current_time() > self.return_end_time(now_time, 60):
                assert exp_text == act_text, "@@@1分钟内检测到预期的提示信息和实际提示信息不一样， 请检查！！！！"
            self.time_sleep(1)

    def confirm_wifi_btn_open(self, timeout=60):
        now = self.get_current_time()
        while True:
            if self.open_wifi_btn():
                break
            if self.get_current_time() > self.return_end_time(now, timeout):
                assert False, "@@@@1分钟内无法打开wifi开关， 请检查!!!!"
            self.time_sleep(1)

    def confirm_wifi_btn_close(self, timeout=60):
        now = self.get_current_time()
        while True:
            if self.close_wifi_btn():
                break
            if self.get_current_time() > self.return_end_time(now, timeout):
                assert False, "@@@@1分钟内无法关闭wifi开关， 请检查!!!!"
            self.time_sleep(1)

    def get_aimdm_logs_list_discard(self):
        cmd = "ls /%s/aimdm/log" % self.get_internal_storage_directory()
        files = self.u2_send_command(cmd)
        files_list = files.split("\n")
        return files_list

    def get_aimdm_logs_list(self):
        cmd = "ls /%s/aimdm/log" % self.get_internal_storage_directory()
        files = self.u2_send_command(cmd)
        files_list = files.split("\n")
        if len(files_list) == 0:
            return []
        return files_list

    def get_logs_txt(self, send_time):
        """
        TPS900+unknown+V1.1.16+20230830.093927_2023_9_21_9_18_16+radio.txt
        TPS900+unknown+V1.1.16+20230830.093927_2023_9_21_9_18_16+main.txt
        """
        logs_list = self.get_aimdm_logs_list()
        generate_list = []
        if len(logs_list) == 0:
            return []
        else:
            logs = logs_list[:-1]
            for log in logs:
                # 20230830.093927_2023_9_21_9_33_7
                log_time = log.split("+")[-2]
                # ['20230830.093927', '2023', '9', '21', '9', '18', '16']
                time_list = self.extract_integers(log_time)
                generate_time = self.format_time(time_list[1:])
                if self.compare_time(send_time, generate_time):
                    generate_list.append(log)
            return generate_list

    def pull_logs_file(self, logs):
        # conf.project_path + "\\Report\\environment.properties"
        internal = self.get_internal_storage_directory()
        des = config.project_path + "\\CatchLogs"
        for txt in logs:
            cmd = "pull /%s/aimdm/log/%s %s" % (internal, txt, des)
            try:
                res = self.send_adb_command(cmd)
                print(res)
            except Exception:
                res = self.send_adb_command(cmd)
                print(res)

    def generate_and_upload_log(self, send_time, file_name):
        logs = self.get_logs_txt(send_time)
        self.pull_logs_file(logs)
        for lo in logs:
            file_path = config.project_path + "\\CatchLogs\\" + lo
            if not self.path_is_existed(file_path):
                assert False, "@@@@无%s文件， 请检查！！！" % lo
            public_pack.allure.attach.file(file_path, name=file_name,
                                           attachment_type=public_pack.allure.attachment_type.TEXT)

    def upload_log(self, file, name):
        public_pack.allure.attach(file, name=name, attachment_type=public_pack.allure.attachment_type.TEXT)

    def manual_unlock(self):
        ele_lock = self.get_element_by_id(self.msg_confirm_id)
        print(ele_lock.get_text())
        try:
            for i in range(6):
                self.click_element(ele_lock)
                print(i)
        except Exception as e:
            print(e)

    def lock_psw_box_presence(self, time_to_wait=3):
        self.wait_ele_presence_by_id(self.lock_psw_id, time_to_wait)

    def lock_psw_input(self, text):
        ele = self.get_element_by_id(self.lock_psw_id)
        self.input_element_text(ele, text)

    def click_psw_confirm_btn(self):
        ele = self.get_element_by_id(self.psw_confirm_id)
        self.click_element(ele)

    def confirm_psw_alert_fade(self, timeout=0):
        now_time = self.get_current_time()
        while True:
            if self.wait_ele_gone_by_id(self.psw_confirm_id, 3):
                return True
            else:
                ele = self.get_element_by_id(self.psw_confirm_id)
                self.click_element(ele)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                return False
            self.time_sleep(1)

    def get_msg_tips_text(self):
        ele = self.get_element_by_id(self.msg_tips_id)
        return self.remove_space(self.get_element_text(ele))

    def get_msg_header_text(self):
        ele = self.get_element_by_id(self.msg_alert_id).child(className=self.msg_header_id)
        return self.remove_space(self.get_element_text(ele))

    def click_msg_confirm_btn(self):
        ele = self.get_element_by_id(self.msg_confirm_id)
        self.click_element(ele)

    def mdm_msg_alert_show(self, time_out=5):
        now_time = self.get_current_time()
        while True:
            ele = self.wait_ele_presence_by_id(self.msg_alert_id, time_out)
            if ele:
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False

    def confirm_alert_show(self, timeout=120):
        now_time = self.get_current_time()
        while True:
            if self.mdm_msg_alert_show():
                break
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@%d内还没弹出弹框， 请检查！！！！" % timeout
            self.time_sleep(1)

    def mdm_msg_alert_show_discard(self, time_out=5):
        now_time = self.get_current_time()
        if not self.wait_alert_appear(self.msg_alert_id, time_out):
            assert False

    def confirm_msg_alert_fade(self, text, timeout=0):
        now_time = self.get_current_time()
        while True:
            ele = self.wait_ele_gone_by_id(self.msg_alert_id, timeout)
            if ele:
                return True
            else:
                # deal with different alert
                if self.get_msg_tips_text() not in self.remove_space(text):
                    return True
                ele = self.get_element_by_id(self.msg_confirm_id)
                self.click_element(ele)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                return False
            self.time_sleep(1)
