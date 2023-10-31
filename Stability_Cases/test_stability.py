import allure
import pytest
import Stability_Cases as st

opt_case = st.Optimize_Case()
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
    wifi_device_info = {"device": device_obj, "ip": device_obj.wlan_ip + ":5555"}
    devices_data.append(wifi_device_info)


class TestStability:
    def setup_class(self):
        self.device_page = st.DevicesPage(test_driver, 40)
        self.app_page = st.APPSPage(test_driver, 40)
        self.content_page = st.ContentPage(test_driver, 40)
        st.MDMPage(test_driver, 40).login_ok(st.yaml_data['website_info']['test_user'],
                                             st.yaml_data['website_info']['test_password'])
        # self.app_page.delete_app_install_and_uninstall_logs()
        self.androids_page = []
        self.devices_sn = []
        self.devices_ip = []

        api_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yml["work_app"]["api_txt"]
        for device_data in devices_data:
            self.android_mdm_page = st.AndroidAimdmPageWiFi(device_data, 5)
            self.android_mdm_page.push_file_to_device(api_path, self.android_mdm_page.get_internal_storage_directory() + "/")
            self.androids_page.append(self.android_mdm_page)
            self.devices_ip.append(device_data["ip"])
            self.android_mdm_page.del_all_content_file()
            self.devices_sn.append(self.android_mdm_page.get_device_sn())
            self.android_mdm_page.del_all_downloaded_apk()
            self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])

    def teardown_class(self):
        pass
        # self.app_page.delete_app_install_and_uninstall_logs()
        # for device_data in devices_data:
        #     self.android_mdm_page = st.AndroidAimdmPageWiFi(device_data, 5)
        #     self.android_mdm_page.del_all_downloaded_apk()
        #     self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        #     self.android_mdm_page.del_all_content_file()
        #     self.app_page.refresh_page()
        #     self.android_mdm_page.reboot_device(device_data["ip"])

    @allure.feature('MDM_stability')
    @allure.title("stability case- 多设备添加--辅助测试用例")
    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_add_multi_devices(self):
        self.device_page.go_to_new_address("devices")
        try:
            # check if device is existed before test, if not, skip
            platform_sn = [self.device_page.remove_space(device["SN"]) for device in self.device_page.get_dev_info_list()]
            print(platform_sn)
            for sn in self.devices_sn:
                devices_list = {"SN": sn, "name": "aut" + sn}
                if sn not in platform_sn:
                    # check if device model is existed, if not, add model
                    info_len_pre = self.device_page.get_dev_info_length()
                    print(info_len_pre)
                    self.device_page.click_new_btn()
                    self.device_page.add_devices_info(devices_list, cate_model=False)
                    self.device_page.get_add_dev_warning_alert()
                    # refresh current Page and clear warning war
                    self.device_page.refresh_page()
                    info_len_pos = self.device_page.get_dev_info_length()
                    print(info_len_pos)
                    assert info_len_pre == info_len_pos - 1
                    # print all devices info
                    print(self.device_page.get_dev_info_list())
        except Exception as e:
            print("发生的异常是", e)
            platform_sn = [self.device_page.remove_space(device["SN"]) for device in
                           self.device_page.get_dev_info_list()]
            print(platform_sn)
            for sn in self.devices_sn:
                devices_list = {"SN": sn, "name": "aut" + sn}
                if sn not in platform_sn:
                    # check if device model is existed, if not, add model
                    info_len_pre = self.device_page.get_dev_info_length()
                    print(info_len_pre)
                    self.device_page.click_new_btn()
                    self.device_page.add_devices_info(devices_list, cate_model=False)
                    # text = self.Page.get_alert_text()
                    # print(text)
                    self.device_page.get_add_dev_warning_alert()
                    # refresh current Page and clear warning war
                    self.device_page.refresh_page()
                    info_len_pos = self.device_page.get_dev_info_length()
                    print(info_len_pos)
                    assert info_len_pre == info_len_pos - 1
                    # print all devices info
                    print(self.device_page.get_dev_info_list())

        # install aimdm apk
        # for android in devices_data
        mdm_app_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yml["work_app"]["aidmd_apk"]
        for t_device in devices_data:
            # install mdm app
            func = st.AndroidAimdmPageWiFi(t_device, 5)
            mdm_app_threads = []
            app_t = st.threading.Thread(target=func.confirm_app_installed, args=(mdm_app_path,))
            app_t.start()
            mdm_app_threads.append(app_t)
            for thread in mdm_app_threads:
                thread.join()
            print("11111111111111111111111111111111111111111111111111")
            mdm_app_threads = []
            app_t = st.threading.Thread(target=func.confirm_app_installed, args=(mdm_app_path,))
            app_t.start()
            mdm_app_threads.append(app_t)
            for thread in mdm_app_threads:
                thread.join()
            print("22222222222222222222222222222222222222222222")
            mdm_reboot_threads = []
            reboot_t = st.threading.Thread(target=func.reboot_device, args=(t_device["ip"],))
            reboot_t.start()
            mdm_app_threads.append(reboot_t)
            for r_thread in mdm_reboot_threads:
                r_thread.join()
        self.device_page.time_sleep(10)
        self.device_page.refresh_page()
        print("333333333333333333333333333333333333333333333")

    @allure.feature('MDM_stability_test')
    @allure.title("stability case- 开机在线成功率--请在报告右侧log文件查看在线率")
    def test_online_stability_test111(self):
        devices_sn = self.devices_sn
        devices_ip = self.devices_ip
        lock = st.threading.Lock()
        length = 1

        device_page = self.device_page
        device_page.go_to_new_address("devices")
        print("444444444444444444444444444444444444444444444444444444")
        # confirm if device is online and execute next step, if not, end the case execution
        for sn in self.devices_sn:
            device_info = opt_case.check_single_device(sn)[0]
            if device_page.upper_transfer("Locked") in device_page.remove_space_and_upper(
                    device_info["Lock Status"]):
                device_page.select_device(sn)
                device_page.click_unlock()
                device_page.refresh_page()
            print("555555555555555555555555555555555")

        def pre_test_clear(td_info):
            if td_info["android_page"].public_alert_show(timeout=5):
                td_info["android_page"].clear_download_and_upgrade_alert()

        def send_devices_message(sns, message):
            # get thread lock
            for sn_ in sns:
                res = opt_case.get_single_device_list(sn_)[0]
                if not device_page.upper_transfer("On") in device_page.remove_space_and_upper(
                        res["Status"]):
                    assert AttributeError
                device_page.refresh_page()
            for sno in sns:
                device_page.select_device(sno)
            device_page.time_sleep(5)
            device_page.click_send_btn()
            device_page.msg_input_and_send(message)

        def check_message_in_device(td_info):
            # check message in device
            td_info["android_page"].screen_keep_on()
            if not td_info["android_page"].public_alert_show(60):
                assert AttributeError
            try:
                td_info["android_page"].confirm_received_text(td_info["message"], timeout=5)
            except AttributeError:
                assert AttributeError
            try:
                td_info["android_page"].click_msg_confirm_btn()
                td_info["android_page"].confirm_msg_alert_fade(td_info["message"])
            except Exception:
                pass

        def test_reboot(td_info):
            td_info["android_page"].reboot_device(td_info["ip"])

        online_flag = 0
        times = 0
        for i in range(length):
            try:
                now = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(st.time.time()))
                msg = "%s:test%d" % (now, times)
                pre_threads = []
                for p_d in range(len(devices_data)):
                    p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[p_d], 5), "sn": devices_sn[p_d],
                             "ip": devices_ip[p_d], "message": msg}
                    pre_t = st.threading.Thread(target=pre_test_clear, args=(p_msg,))
                    pre_t.start()
                    pre_threads.append(pre_t)
                for thread in pre_threads:
                    thread.join()

                # send message
                device_page.refresh_page()
                send_devices_message(devices_sn, msg)

                times += 1
                check_message_threads = []
                for c_d in range(len(devices_data)):
                    p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[c_d], 5), "sn": devices_sn[c_d],
                             "ip": devices_ip[c_d], "message": msg}
                    check_t = st.threading.Thread(target=check_message_in_device, args=(p_msg,))
                    check_t.start()
                    check_message_threads.append(check_t)
                for thread in check_message_threads:
                    thread.join()

                # reboot device
                check_reboot_threads = []
                for c_d in range(len(devices_data)):
                    p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[c_d], 5), "sn": devices_sn[c_d],
                             "ip": devices_ip[c_d], "message": msg}
                    check_r = st.threading.Thread(target=test_reboot, args=(p_msg,))
                    check_r.start()
                    check_reboot_threads.append(check_r)
                for thread in check_reboot_threads:
                    thread.join()

                device_page.refresh_page()
                send_devices_message(devices_sn, msg)

                # check message after device
                times += 1
                check_message_reboot_threads = []
                for c_d in range(len(devices_data)):
                    p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[c_d], 5), "sn": devices_sn[c_d],
                             "ip": devices_ip[c_d], "message": msg}
                    check_m = st.threading.Thread(target=check_message_in_device, args=(p_msg,))
                    check_m.start()
                    check_message_reboot_threads.append(check_m)
                for thread in check_message_reboot_threads:
                    thread.join()
                online_flag += 1
            except Exception as e:
                print(e)
                log.error(str(e))
                continue

        print(online_flag)
        msg = "重启%d次1分钟内在线成功率为%s" % (length, str(online_flag / length))
        log.info(msg)
        print(msg)


