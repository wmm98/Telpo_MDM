import Page as public_pack
from Page.Android_Base_Page_USB import AndroidBasePageUSB
from Page.Android_Base_Page_WiFi import AndroidBasePageWiFi


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
    msg_alert_id = "%s:id/root_view" % aimdm_package

    # lock alert, input device psw relate
    lock_psw_id = "%s:id/et_pwd" % aimdm_package
    psw_confirm_id = "%s:id/confirm_pwd" % aimdm_package

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

    def get_aimdm_logs_list(self):
        cmd = "ls /%s/aimdm/log" % self.get_internal_storage_directory()
        files = self.u2_send_command(cmd)
        files_list = files.split("\n")
        return files_list

    def manual_unlock(self):
        # ele = self.get_element_by_id(self.msg_confirm_id)
        # ele = self.client(resourceId=self.msg_confirm_id)
        ele = self.get_element_by_id_no_wait(self.msg_confirm_id)
        print(ele.get_text())
        try:
            for i in range(10):
                ele.click()
                self.time_sleep(0.2)
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
