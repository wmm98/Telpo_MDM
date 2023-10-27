import allure
import Stability_Cases as st

conf = st.Config()
log = st.Log.MyLog()
wifi_adb = st.WIFIADBConnect()
test_yml = st.yaml_data
# alert = AlertData()

#
# # 先进行登录
web = st.BaseWebDriver()
test_driver = web.get_web_driver()
ips = st.lan_ips.get_ips_list()
devices = [wifi_adb.wifi_connect_device(ip_) for ip_ in ips]
devices_data = []
for device_obj in devices:
    wifi_device_info = {"device": device_obj, "ip": device_obj.wlan_ip + ":55555"}
    devices_data.append(wifi_device_info)


class TestStability:
    def setup_class(self):
        self.device_page = st.DevicesPage(test_driver, 40)
        self.app_page = st.APPSPage(test_driver, 40)
        self.content_page = st.ContentPage(test_driver, 40)
        for device_data in devices_data:
            self.android_mdm_page = st.AndroidAimdmPageWiFi(device_data, 5)
            # self.wifi_ip = device_data["wifi_device_info"]["ip"]
            self.android_mdm_page.del_all_content_file()
            # self.device_sn = self.android_mdm_page.get_device_sn()
            self.app_page.delete_app_install_and_uninstall_logs()
            self.android_mdm_page.del_all_downloaded_apk()
            self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        # self.android_mdm_page.del_all_downloaded_apk()
        # self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        # self.android_mdm_page.del_all_content_file()
        # self.app_page.refresh_page()
        # self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_stability_test')
    @allure.title("stability case- 开机在线成功率--请在报告右侧log文件查看在线率")
    def test_online_stability_test1(self):
        pass

    @allure.feature('MDM_stability_test1')
    @allure.title("stability case- 开机在线成功率--请在报告右侧log文件查看在线率")
    def test_online_stability_test(self):
        sn = self.device_sn
        length = 50
        self.device_page.refresh_page()
        # confirm if device is online and execute next step, if not, end the case execution
        data = opt_case.check_single_device(sn)
        print(data)
        now = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(case_pack.time.time()))
        online_flag = 0
        for i in range(length):
            if self.android_mdm_page.public_alert_show(3):
                self.android_mdm_page.clear_download_and_upgrade_alert()
            self.device_page.refresh_page()
            msg = "%s:test%d" % (now, i)
            device_info = opt_case.get_single_device_list(sn)[0]
            if self.device_page.upper_transfer("on") in self.device_page.remove_space_and_upper(device_info["Status"]):
                if self.device_page.upper_transfer("Locked") in self.device_page.remove_space_and_upper(
                        device_info["Lock Status"]):
                    self.device_page.select_device(sn)
                    self.device_page.click_unlock()
                    self.device_page.refresh_page()
                self.device_page.select_device(sn)
                self.device_page.click_send_btn()
                self.device_page.msg_input_and_send(msg)
                # message_list.append(msg)
                # check message in device
                if not self.android_mdm_page.public_alert_show(60):
                    continue
                try:
                    self.android_mdm_page.confirm_received_text(msg, timeout=5)
                except AttributeError:
                    continue
                try:
                    self.android_mdm_page.click_msg_confirm_btn()
                    self.android_mdm_page.confirm_msg_alert_fade(msg)
                except Exception:
                    pass
            self.android_mdm_page.reboot_device(self.wifi_ip)
            if self.android_mdm_page.public_alert_show(timeout=5):
                self.android_mdm_page.clear_download_and_upgrade_alert()
            self.device_page.refresh_page()
            device_info_after_reboot = opt_case.get_single_device_list(sn)[0]
            if self.device_page.upper_transfer("on") in self.device_page.remove_space_and_upper(
                    device_info_after_reboot["Status"]):
                self.device_page.select_device(sn)
                self.device_page.click_send_btn()
                self.device_page.msg_input_and_send(msg)
                # message_list.append(msg)
                # check message in device
                if not self.android_mdm_page.public_alert_show(60):
                    continue
                try:
                    self.android_mdm_page.confirm_received_text(msg, timeout=5)
                except AttributeError:
                    continue
                try:
                    self.android_mdm_page.click_msg_confirm_btn()
                    self.android_mdm_page.confirm_msg_alert_fade(msg)
                except Exception:
                    pass
            online_flag += 1
            self.device_page.refresh_page()
        print(online_flag)
        msg = "重启%d次1分钟内在线成功率为%s" % (length, str(online_flag / length))
        log.info(msg)
        print(msg)
