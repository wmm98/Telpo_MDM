import allure
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
        self.app_page.delete_app_install_and_uninstall_logs()
        self.androids_page = []
        self.devices_sn = []
        self.devices_ip = []
        for device_data in devices_data:
            self.android_mdm_page = st.AndroidAimdmPageWiFi(device_data, 5)
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
    @allure.title("stability case- 开机在线成功率--请在报告右侧log文件查看在线率")
    def test_online(self):
        assert True

    @allure.feature('MDM_stability_test')
    @allure.title("stability case- 开机在线成功率--请在报告右侧log文件查看在线率")
    def test_online_stability_test(self):
        devices_sn = self.devices_sn
        devices_ip = self.devices_ip
        lock = st.threading.Lock()
        online_flag = 0
        length = 1
        self.device_page.refresh_page()
        device_page = self.device_page
        # confirm if device is online and execute next step, if not, end the case execution
        for sn in self.devices_sn:
            opt_case.check_single_device(sn)

        # param = {"android_page": td, "sn": sn, "ip": ip}
        def pressure_test(td_info):
            now = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(st.time.time()))
            for i in range(length):
                if td_info["android_page"].public_alert_show(3):
                    td_info["android_page"].clear_download_and_upgrade_alert()
                msg = "%s:test%d" % (now, i)
                # get thread lock
                lock.acquire()
                device_page.refresh_page()
                device_info = opt_case.get_single_device_list(td_info["sn"])[0]
                if device_page.upper_transfer("on") in device_page.remove_space_and_upper(
                        device_info["Status"]):
                    if device_page.upper_transfer("Locked") in device_page.remove_space_and_upper(
                            device_info["Lock Status"]):
                        device_page.select_device(td_info["sn"])
                        device_page.click_unlock()
                        device_page.refresh_page()
                    device_page.select_device(td_info["sn"])
                    device_page.click_send_btn()
                    device_page.msg_input_and_send(msg)
                    # unlock thread
                    lock.release()
                    # check message in device
                    td_info["android_page"].screen_keep_on()
                    if not td_info["android_page"].public_alert_show(60):
                        continue
                    # try:
                    td_info["android_page"].confirm_received_text(msg, timeout=5)
                    # except AttributeError:
                    #     continue
                    # try:
                    td_info["android_page"].click_msg_confirm_btn()
                    td_info["android_page"].confirm_msg_alert_fade(msg)
                    # except Exception:
                    #     pass
                td_info["android_page"].reboot_device(td_info["ip"])
                if td_info["android_page"].public_alert_show(timeout=5):
                    td_info["android_page"].clear_download_and_upgrade_alert()
                device_page.refresh_page()
                # get lock
                lock.acquire()
                device_info_after_reboot = opt_case.get_single_device_list(td_info["sn"])[0]
                if device_page.upper_transfer("on") in device_page.remove_space_and_upper(
                        device_info_after_reboot["Status"]):
                    device_page.select_device(td_info["sn"])
                    device_page.click_send_btn()
                    device_page.msg_input_and_send(msg)
                    lock.release()
                    # check message in device
                    td_info["android_page"].screen_keep_on()
                    if not td_info["android_page"].public_alert_show(60):
                        continue
                    try:
                        td_info["android_page"].confirm_received_text(msg, timeout=5)
                    except AttributeError:
                        continue
                    try:
                        td_info["android_page"].click_msg_confirm_btn()
                        td_info["android_page"].confirm_msg_alert_fade(msg)
                    except Exception:
                        pass
                # online_flag += 1
                device_page.refresh_page()

        threads = []
        for p_d in range(len(devices_data)):
            p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[p_d], 5), "sn": devices_sn[p_d],
                     "ip": devices_ip[p_d]}
            t = st.threading.Thread(target=pressure_test, args=(p_msg,))
            t.start()
            threads.append(t)
        # wait all threads finish
        for thread in threads:
            thread.join()

        # print(online_flag)
        # msg = "重启%d次1分钟内在线成功率为%s" % (length, str(online_flag / length))
        # log.info(msg)
        # print(msg)

    @allure.feature('MDM_stability_test11')
    @allure.title("stability case- 开机在线成功率--请在报告右侧log文件查看在线率")
    def test_online_stability_test111(self):
        devices_sn = self.devices_sn
        devices_ip = self.devices_ip
        lock = st.threading.Lock()
        online_flag = 0
        length = 1
        self.device_page.refresh_page()
        device_page = self.device_page
        # confirm if device is online and execute next step, if not, end the case execution
        for sn in self.devices_sn:
            device_info = opt_case.check_single_device(sn)
            if device_page.upper_transfer("Locked") in device_page.remove_space_and_upper(
                    device_info["Lock Status"]):
                device_page.select_device(sn)
                device_page.click_unlock()
                device_page.refresh_page()

        def pre_test_clear(td_info):
            if td_info["android_page"].public_alert_show(timeout=5):
                td_info["android_page"].clear_download_and_upgrade_alert()

        def send_devices_message(sns):
            # get thread lock
            device_page.refresh_page()
            for sn_ in sns:
                res = opt_case.get_single_device_list(sn_)[0]
            if device_page.upper_transfer("on") in device_page.remove_space_and_upper(
                    device_info["Status"]):
                device_page.select_device(td_info["sn"])
                device_page.click_send_btn()
                device_page.msg_input_and_send(msg)

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

        # param = {"android_page": td, "sn": sn, "ip": ip}
        # def pressure_test(td_info):
        #     now = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(st.time.time()))
        #     for i in range(length):
        #         if td_info["android_page"].public_alert_show(3):
        #             td_info["android_page"].clear_download_and_upgrade_alert()
        #         msg = "%s:test%d" % (now, i)
        #         # get thread lock
        #         lock.acquire()
        #         device_page.refresh_page()
        #         device_info = opt_case.get_single_device_list(td_info["sn"])[0]
        #         if device_page.upper_transfer("on") in device_page.remove_space_and_upper(
        #                 device_info["Status"]):
        #             if device_page.upper_transfer("Locked") in device_page.remove_space_and_upper(
        #                     device_info["Lock Status"]):
        #                 device_page.select_device(td_info["sn"])
        #                 device_page.click_unlock()
        #                 device_page.refresh_page()
        #             device_page.select_device(td_info["sn"])
        #             device_page.click_send_btn()
        #             device_page.msg_input_and_send(msg)
        #             # unlock thread
        #             lock.release()
        #             # check message in device
        #             td_info["android_page"].screen_keep_on()
        #             if not td_info["android_page"].public_alert_show(60):
        #                 continue
        #             # try:
        #             td_info["android_page"].confirm_received_text(msg, timeout=5)
        #             # except AttributeError:
        #             #     continue
        #             # try:
        #             td_info["android_page"].click_msg_confirm_btn()
        #             td_info["android_page"].confirm_msg_alert_fade(msg)
        #             # except Exception:
        #             #     pass
        #         td_info["android_page"].reboot_device(td_info["ip"])
        #         if td_info["android_page"].public_alert_show(timeout=5):
        #             td_info["android_page"].clear_download_and_upgrade_alert()
        #         device_page.refresh_page()
        #         # get lock
        #         lock.acquire()
        #         device_info_after_reboot = opt_case.get_single_device_list(td_info["sn"])[0]
        #         if device_page.upper_transfer("on") in device_page.remove_space_and_upper(
        #                 device_info_after_reboot["Status"]):
        #             device_page.select_device(td_info["sn"])
        #             device_page.click_send_btn()
        #             device_page.msg_input_and_send(msg)
        #             lock.release()
        #             # check message in device
        #             td_info["android_page"].screen_keep_on()
        #             if not td_info["android_page"].public_alert_show(60):
        #                 continue
        #             try:
        #                 td_info["android_page"].confirm_received_text(msg, timeout=5)
        #             except AttributeError:
        #                 continue
        #             try:
        #                 td_info["android_page"].click_msg_confirm_btn()
        #                 td_info["android_page"].confirm_msg_alert_fade(msg)
        #             except Exception:
        #                 pass
        #         # online_flag += 1
        #         device_page.refresh_page()

        pre_threads = []

        for i in range(length):
            now = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(st.time.time()))
            msg = "%s:test%d" % (now, i)
            for p_d in range(len(devices_data)):
                p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[p_d], 5), "sn": devices_sn[p_d],
                         "ip": devices_ip[p_d], "message": msg}
                pre_t = st.threading.Thread(target=pre_test_clear, args=(p_msg,))
                pre_t.start()
                pre_threads.append(pre_t)

            for thread in pre_threads:
                thread.join()
            send_devices_message(p_msg)

        # print(online_flag)
        # msg = "重启%d次1分钟内在线成功率为%s" % (length, str(online_flag / length))
        # log.info(msg)
        # print(msg)
