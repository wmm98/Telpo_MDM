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
        self.ota_page = st.OTAPage(test_driver, 40)
        self.mdm_page = st.MDMPage(test_driver, 40)
        self.app_page.delete_app_install_and_uninstall_logs()
        self.content_page.delete_all_content_release_log()
        self.ota_page.delete_all_ota_release_log()
        self.androids_page = []
        self.devices_sn = []
        self.devices_ip = []

        api_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yml["work_app"]["api_txt"]
        for device_data in devices_data:
            self.android_mdm_page = st.AndroidAimdmPageWiFi(device_data, 5)
            self.androids_page.append(self.android_mdm_page)
            self.devices_ip.append(device_data["ip"])
            self.android_mdm_page.del_all_content_file()
            self.devices_sn.append(self.android_mdm_page.get_device_sn())
            self.android_mdm_page.del_all_downloaded_apk()
            self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
            self.android_mdm_page.push_file_to_device(api_path,
                                                      self.android_mdm_page.get_internal_storage_directory() + "/")
        pre_del_apk_thread = []
        pre_uninstall_apps_thread = []
        pre_del_updated_file_thread = []
        pre_reboot_thread = []
        for android_ in self.androids_page:
            pre_d_apk_t = st.threading.Thread(target=android_.del_all_downloaded_apk(), args=())
            pre_d_apk_t.start()
            pre_del_apk_thread.append(pre_d_apk_t)

            pre_uninstall_t = st.threading.Thread(target=android_.uninstall_multi_apps, args=(test_yml['app_info'],))
            pre_uninstall_t.start()
            pre_uninstall_apps_thread.append(pre_uninstall_t)

            pre_del_update_t = st.threading.Thread(target=android_.del_updated_zip, args=())
            pre_del_update_t.start()
            pre_del_updated_file_thread.append(pre_del_update_t)

            pre_r_t = st.threading.Thread(target=android_.reboot_device, args=(android_.device_ip,))
            pre_r_t.start()
            pre_reboot_thread.append(pre_r_t)

        for i in range(len(pre_del_apk_thread)):
            pre_del_apk_thread[i].join()
            pre_uninstall_apps_thread[i].join()
            pre_del_updated_file_thread[i].join()
            pre_reboot_thread[i].join()

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        self.ota_page.delete_all_ota_release_log()
        pos_del_apk_thread = []
        uninstall_apps_thread = []
        pos_del_content_thread = []
        pos_reboot_thread = []
        for device_data in devices_data:
            self.android_mdm_page = st.AndroidAimdmPageWiFi(device_data, 5)
            pos_d_apk_t = st.threading.Thread(target=self.android_mdm_page.del_all_downloaded_apk(), args=())
            pos_d_apk_t.start()
            pos_del_apk_thread.append(pos_d_apk_t)

            pos_uninstall_t = st.threading.Thread(target=self.android_mdm_page.uninstall_multi_apps,
                                                  args=(test_yml['app_info'],))
            pos_uninstall_t.start()
            uninstall_apps_thread.append(pos_uninstall_t)

            pos_del_content_t = st.threading.Thread(target=self.android_mdm_page.del_all_content_file, args=())
            pos_del_content_t.start()
            pos_del_content_thread.append(pos_del_content_t)

            self.android_mdm_page.del_all_downloaded_apk()
            self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
            self.android_mdm_page.del_all_content_file()
            self.android_mdm_page.reboot_device(device_data["ip"])
            r_t = st.threading.Thread(target=self.android_mdm_page.reboot_device, args=(device_data["ip"],))
            r_t.start()
            pos_reboot_thread.append(r_t)

        for j in range(len(pos_del_apk_thread)):
            pos_del_apk_thread[j].join()
            uninstall_apps_thread[j].join()
            pos_del_content_thread[j].join()
            pos_reboot_thread[j].join()

        self.app_page.refresh_page()

    @allure.feature('MDM_stability—login')
    @allure.title("stability case- 登录--辅助测试用例")
    def test_stability_login(self):
        username = st.yaml_data['website_info']['test_user']
        password = st.yaml_data['website_info']['test_password']

        self.mdm_page.login_ok(username, password)
        now_time = self.app_page.get_current_time()
        while True:
            try:
                if self.mdm_page.web_driver_wait_until(st.EC.url_contains("device"), 10):
                    break
            except Exception:
                pass
            if self.mdm_page.get_current_time() > self.mdm_page.return_end_time(now_time):
                assert False, "无法登录，请检查！！！"
            self.mdm_page.refresh_page()
            self.mdm_page.login_ok(username, password)

    @allure.feature('MDM_stability1')
    @allure.title("stability case- 多设备添加--辅助测试用例")
    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_add_multi_devices(self):
        self.device_page.go_to_new_address("devices")
        try:
            # check if device is existed before test, if not, skip
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
        mdm_app_threads = []
        mdm_app_installed_threads = []
        mdm_reboot_threads = []
        mdm_app_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yml["work_app"]["aidmd_apk"]
        for t_device in devices_data:
            # install mdm app
            func = st.AndroidAimdmPageWiFi(t_device, 5)

            app_t = st.threading.Thread(target=func.confirm_app_installed, args=(mdm_app_path,))
            app_t.start()
            mdm_app_threads.append(app_t)

            app_t = st.threading.Thread(target=func.confirm_app_installed, args=(mdm_app_path,))
            app_t.start()
            mdm_app_installed_threads.append(app_t)

            reboot_t = st.threading.Thread(target=func.reboot_device, args=(t_device["ip"],))
            reboot_t.start()
            mdm_app_threads.append(reboot_t)

        for app_thread in mdm_app_threads:
            app_thread.join()
        for inst_thread in mdm_app_installed_threads:
            inst_thread.join()
        for r_thread in mdm_reboot_threads:
            r_thread.join()
        self.device_page.time_sleep(3)
        self.device_page.refresh_page()

    @allure.feature('MDM_stability_test')
    @allure.title("stability case- 重启在线成功率--请在报告右侧log文件查看在线率")
    def test_reboot_online_stability_test(self):
        devices_sn = self.devices_sn
        devices_ip = self.devices_ip

        length = 1
        device_page = self.device_page
        device_page.go_to_new_address("devices")
        # confirm if device is online and execute next step, if not, end the case execution
        for sn in self.devices_sn:
            device_info = opt_case.check_single_device(sn)[0]
            if device_page.upper_transfer("Locked") in device_page.remove_space_and_upper(
                    device_info["Lock Status"]):
                device_page.select_device(sn)
                device_page.click_unlock()
            device_page.refresh_page()

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

    @allure.feature('MDM_stability_test')
    @allure.title("stability case-文件文件推送成功率-请在报告右侧log文件查看文件文件推送成功率")
    def test_multi_release_debug(self):
        self.content_page.go_to_new_address("content/log")
        self.content_page.search_upgrade_log_by_sn(self.devices_sn[0])

    @allure.feature('MDM_stability_test111')
    @allure.title("stability case-文件文件推送成功率-请在报告右侧log文件查看文件文件推送成功率")
    def test_multi_release_content(self):
        # lock = st.threading.Lock()
        lock = st.threading.Lock()
        devices_sn = self.devices_sn
        devices_ip = self.devices_ip
        print(devices_ip)
        content_page = self.content_page
        stability_files = test_yml["Content_info"]["stability_test_file"]
        for sn in self.devices_sn:
            opt_case.check_single_device(sn)

        release_to_path = "%s/aimdm" % self.android_mdm_page.get_internal_storage_directory()
        grep_cmd = "ls %s" % release_to_path
        release_flag = 0
        for file in stability_files:
            # release normal file
            if file in self.android_mdm_page.u2_send_command(grep_cmd):
                self.android_mdm_page.rm_file("%s/%s" % (release_to_path, file))
                self.android_mdm_page.rm_file("%s/%s" % (release_to_path, file))

            self.content_page.go_to_new_address("content")
            file_path = conf.project_path + "\\Param\\Content\\%s" % file
            file_size = self.content_page.get_file_size_in_windows(file_path)
            print("获取到的文件 的size(bytes): ", file_size)
            file_hash_value = self.android_mdm_page.calculate_sha256_in_windows(file, directory="Content")
            print("file_hash_value:", file_hash_value)
            send_time = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(self.content_page.get_current_time()))
            self.content_page.time_sleep(4)
            self.content_page.search_content('Normal Files', file)
            release_info = {"sn": self.devices_sn, "content_name": file}
            self.content_page.time_sleep(4)
            assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有相关文件： %s, 请检查" % file
            self.content_page.release_content_file(release_info["sn"], file_path=release_to_path)
            # check release log
            self.content_page.go_to_new_address("content/release")
            self.content_page.time_sleep(3)
            now_time = self.content_page.get_current_time()
            while True:
                release_len = self.content_page.get_current_content_release_log_total()
                print("release_len", release_len)
                if release_len == len(release_info["sn"]) + release_flag:
                    break
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                    assert False, "@@@@没有相应的文件 release log， 请检查！！！"
                self.content_page.time_sleep(3)
                self.content_page.refresh_page()

            print("**********************释放log检测完毕*************************************")

            def check_devices_download_file(device_msg):
                device_msg["android_page"].screen_keep_on()
                # check the content download record in device
                now_time = content_page.get_current_time()
                while True:
                    if device_msg["android_page"].download_file_is_existed(file):
                        break
                    if content_page.get_current_time() > content_page.return_end_time(now_time, 1800):
                        assert False, "@@@@应用推送中超过30分钟还没有%s的下载记录" % file
                    content_page.time_sleep(3)
                print("**********************下载记录检测完毕*************************************")

                before_reboot_file_size = device_msg["android_page"].get_file_size_in_device(file)
                print("第一次下载的的file size: ", before_reboot_file_size)
                for i in range(1):
                    device_msg["android_page"].reboot_device(device_msg["ip"])
                    now_time = content_page.get_current_time()
                    while True:
                        current_size = device_msg["android_page"].get_file_size_in_device(file)
                        print("重启%s次之后当前file 的size: %s" % (str(i + 1), current_size))
                        if current_size == file_size:
                            assert False, "@@@@文件太小，请上传大附件！！！！"
                        if current_size > before_reboot_file_size:
                            before_reboot_file_size = current_size
                            break
                        if content_page.get_current_time() > content_page.return_end_time(now_time, 120):
                            assert False, "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载"
                        content_page.time_sleep(1)
                print("*******************完成5次重启*********************************")
                # check if app download completed in the settings time
                now_time = content_page.get_current_time()
                while True:
                    shell_hash_value = device_msg["android_page"].calculate_sha256_in_device(file)
                    if file_hash_value == shell_hash_value:
                        break
                    if content_page.get_current_time() > content_page.return_end_time(now_time, 1800):
                        assert False, "@@@@推送中超过30分钟还没有完成%s的下载" % file
                    content_page.time_sleep(3)
                print("**********************下载完成检测完毕*************************************")
                lock.acquire()
                content_page.go_to_new_address("content/log")
                now_time_ = content_page.get_current_time()
                while True:
                    content_page.search_upgrade_log_by_sn(device_msg["sn"])
                    upgrade_list = content_page.get_content_latest_upgrade_log(send_time, device_msg)
                    print("upgrade_list: ", upgrade_list)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        print("action", action)
                        if content_page.get_action_status(action) == 7:
                            break
                    # wait upgrade 3 min at most
                    if content_page.get_current_time() > content_page.return_end_time(now_time_, 60):
                        assert False, "@@@@3分钟还没有设置完相应的文件， 请检查！！！"
                    content_page.time_sleep(5)
                    content_page.refresh_page()
                # content_page.go_to_new_address("content/log")
                lock.release()
                assert file in device_msg["android_page"].u2_send_command(
                    grep_cmd), "@@@@文件没有释放到设备指定的路径%s, 请检查！！！" % release_to_path
                print("***************************************设备%s完成文件%s的推送*********************************" % (
                    device_msg["ip"], file))

            # release file to multi devices
            contents_threads = []
            for content_i in range(len(ips)):
                content_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[content_i], 5),
                               "sn": devices_sn[content_i], "ip": devices_ip[content_i], "content_name": file}
                content_t = st.threading.Thread(target=check_devices_download_file, args=(content_msg,))
                content_t.start()
                contents_threads.append(content_t)
            for thread in contents_threads:
                thread.join()

            # check_message_reboot_threads = []
            # for c_d in range(len(devices_data)):
            #     p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[c_d], 5), "sn": devices_sn[c_d],
            #              "ip": devices_ip[c_d], "message": msg}
            #     check_m = st.threading.Thread(target=check_message_in_device, args=(p_msg,))
            #     check_m.start()
            #     check_message_reboot_threads.append(check_m)
            # for thread in check_message_reboot_threads:
            #     thread.join()

    @allure.feature('MDM_stability_test')
    @allure.title("stability case- 长时间连接测试--长时间连接测试，并且静默升级OTA升级")
    def test_online_long_test(self):
        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.devices_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        file_path = self.app_page.get_apk_path(release_info["package_name"])
        package = self.app_page.get_apk_package_name(file_path)
        release_info["package"] = package
        print("包名：", package)
        version = self.app_page.get_apk_package_version(file_path)
        release_info["version"] = version
        devices_sn = self.devices_sn
        devices_ip = self.devices_ip
        length = 2
        lock = st.threading.Lock()
        app_page = self.app_page
        device_page = self.device_page

        reboot_threads = []
        for android in self.androids_page:
            r_t = st.threading.Thread(target=android.reboot_device, args=(android.device_ip,))
            r_t.start()
            reboot_threads.append(r_t)
        for r_thread in reboot_threads:
            r_thread.join()

        device_page.go_to_new_address("devices")
        # confirm if device is online and execute next step, if not, end the case execution
        for sn in self.devices_sn:
            device_info = opt_case.check_single_device(sn)[0]
            if device_page.upper_transfer("Locked") in device_page.remove_space_and_upper(
                    device_info["Lock Status"]):
                device_page.select_device(sn)
                device_page.click_unlock()
                device_page.refresh_page()

        def pre_test_clear(td_info):
            if td_info["android_page"].public_alert_show(timeout=5):
                td_info["android_page"].clear_download_and_upgrade_alert()

        # clear alert in device
        now = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(st.time.time()))
        msg = "%s:test" % now
        pre_threads = []
        for p_d in range(len(devices_data)):
            p_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[p_d], 5), "sn": devices_sn[p_d],
                     "ip": devices_ip[p_d], "message": msg}
            pre_t = st.threading.Thread(target=pre_test_clear, args=(p_msg,))
            pre_t.start()
            pre_threads.append(pre_t)
        for thread in pre_threads:
            thread.join()

        def send_devices_message(sns, message):
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

                online_flag += 1
            except Exception as e:
                print(e)
                log.error(str(e))
                continue
            device_page.time_sleep(10)

        print(online_flag)
        msg = "%ds内在线成功率为%s" % (length * 60, str(online_flag / length))
        log.info(msg)
        print(msg)

        print("================================在线状态测完===================================")
        log.info("================================在线状态测完===================================")
        print("****************************长时间挂机后静默安装测试*******************************")
        log.info("****************************长时间挂机后静默安装测试*******************************")

        # release_app
        send_time = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(self.app_page.get_current_time()))
        self.app_page.time_sleep(5)
        self.app_page.go_to_new_address("apps")
        self.app_page.search_app_by_name(release_info["package_name"])
        app_list = self.app_page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.app_page.click_release_app_btn()
        self.app_page.input_release_app_info(release_info)

        # go to app release log
        self.app_page.go_to_new_address("apps/releases")
        now_time = self.app_page.get_current_time()
        while True:
            if self.app_page.get_current_app_release_log_total() == len(release_info["sn"]):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
                assert False, "@@@@超过3分钟没有相应的 app release log， 请检查！！！"
            self.app_page.time_sleep(3)

        # silent install app
        def check_devices_install_app(device_msg):
            # self.android_mdm_page.reboot_device(device_msg["ip"])
            # self.app_page.refresh_page()

            print("**********************释放log检测完毕*************************************")
            # check the app download record in device
            original_hash_value = device_msg["android_page"].calculate_sha256_in_windows(release_info["package_name"])
            shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
            now_time = app_page.get_current_time()
            while True:
                if device_msg["android_page"].download_file_is_existed(shell_app_apk_name):
                    break
                if app_page.get_current_time() > app_page.return_end_time(now_time, 1800):
                    assert False, "@@@@应用推送中超过30分钟还没有%s的下载记录" % release_info["package_name"]
                app_page.time_sleep(3)
            print("**********************下载记录检测完毕*************************************")

            # check if app download completed in the settings time
            # file_path = conf.project_path + "\\Param\\Package\\"
            now_time = app_page.get_current_time()
            while True:
                shell_hash_value = device_msg["android_page"].calculate_sha256_in_device(shell_app_apk_name)
                if original_hash_value == shell_hash_value:
                    break
                if app_page.get_current_time() > app_page.return_end_time(now_time, 1800):
                    assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                app_page.time_sleep(3)
            print("**********************下载完成检测完毕*************************************")

            # check if app installed in settings time
            now_time = app_page.get_current_time()
            while True:
                if device_msg["android_page"].app_is_installed(release_info["package"]):
                    break
                if app_page.get_current_time() > app_page.return_end_time(now_time, 180):
                    assert False, "@@@@多应用推送中超过3分钟还没有%s的安装记录" % release_info["package_name"]
            print("******************************安装记录检测完毕****************************************")
            lock.acquire()
            # check if all installed success logs in app upgrade logs
            app_page.go_to_new_address("apps/logs")
            now_time = app_page.get_current_time()
            while True:
                app_page.search_upgrade_logs(device_msg["package"], device_msg["sn"])
                upgrade_list = app_page.get_app_latest_upgrade_log(send_time, device_msg)
                if len(upgrade_list) != 0:
                    action = upgrade_list[0]["Action"]
                    print(action)
                    if app_page.get_action_status(action) == 4:
                        break
                if app_page.get_current_time() > app_page.return_end_time(now_time, 300):
                    assert False, "@@@@多应用推送中设备已经安装完毕app, 平台超过5分钟还上报%s的安装记录" % release_info["package_name"]
                app_page.time_sleep(5)
                app_page.refresh_page()
            print(
                "***************************************设备%s安装上报完成*********************************" % device_msg["ip"])
            lock.release()

        # multi threads install app
        install_threads = []
        for p_d in range(len(devices_data)):
            inst_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[p_d], 5), "sn": devices_sn[p_d],
                        "ip": devices_ip[p_d], "package": release_info["package"], "version": release_info["version"]}
            inst_t = st.threading.Thread(target=check_devices_install_app, args=(inst_msg,))
            inst_t.start()
            install_threads.append(inst_t)
        for i_thread in install_threads:
            i_thread.join()
        print("*****************************静默安装完成*****************************")
        log.info("*****************************静默安装完成*****************************")
        # multi threads upgrade ota package
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": devices_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        # get release ota package version
        ota_page = self.ota_page
        release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])

        def check_current_upgrade_firmware(and_device):
            current_firmware_version = and_device.check_firmware_version()
            # compare current version and exp version
            assert ota_page.transfer_version_into_int(current_firmware_version) < ota_page.transfer_version_into_int(
                release_info["version"]), \
                "@@@@%s释放的ota升级包比当前固件版本版本低， 请检查！！！" % and_device.device_ip

        check_firmware_thread = []
        for android_p in self.androids_page:
            firm_t = st.threading.Thread(target=check_current_upgrade_firmware, args=(android_p,))
            firm_t.start()
            check_firmware_thread.append(firm_t)
        for f_thread in check_firmware_thread:
            f_thread.join()
        # get ota size in windows and device
        print("ota after upgrade version:", release_info["version"])
        # check file size and hash value in directory Param/package
        ota_package_path = self.ota_page.get_apk_path(release_info["package_name"])
        act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
        print("act_ota_package_size:", act_ota_package_size)
        # check file hash value in directory Param/package
        act_ota_package_hash_value = self.ota_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_ota_package_hash_value)

        # release ota package
        self.ota_page.go_to_new_address("ota")
        self.ota_page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        send_time = st.time.strftime('%Y-%m-%d %H:%M', st.time.localtime(self.ota_page.get_current_time()))
        print("send_time", send_time)
        self.ota_page.time_sleep(5)

        # if device is existed, click
        self.ota_page.click_release_btn()
        try:
            self.ota_page.input_release_OTA_package(release_info)
        except Exception as e:
            print(e)
        self.ota_page.go_to_new_address("ota/release")
        now_time = self.ota_page.get_current_time()
        # check release logs
        while True:
            if self.ota_page.get_current_ota_release_log_total() == len(release_info["sn"]):
                break
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time):
                assert False, "@@@@没有相应的 ota package release log， 请检查！！！"
            self.ota_page.time_sleep(3)
            self.ota_page.refresh_page()
        print("**********************释放log检测完毕*************************************")

        def check_devices_upgrade_ota_package(device_msg):
            device_msg["android_page"].screen_keep_on()
            device_msg["android_page"].confirm_received_alert(download_tips)
            device_current_firmware_version = device_msg["android_page"].check_firmware_version()
            # check the app download record in device
            now_time = ota_page.get_current_time()
            while True:
                if device_msg["android_page"].download_file_is_existed(device_msg["package_name"]):
                    break
                if ota_page.get_current_time() > ota_page.return_end_time(now_time, 1800):
                    assert False, "@@@@应用推送中超过30分钟还没有%s的下载记录" % device_msg["package_name"]
                ota_page.time_sleep(3)
            print("**********************下载记录检测完毕*************************************")

            # check if app download completed in the settings time
            # file_path = conf.project_path + "\\Param\\Package\\"
            now_time = ota_page.get_current_time()
            while True:
                shell_hash_value = device_msg["android_page"].calculate_sha256_in_device(device_msg["package_name"])
                if act_ota_package_hash_value == shell_hash_value:
                    break
                if ota_page.get_current_time() > ota_page.return_end_time(now_time, 1800):
                    assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                ota_page.time_sleep(3)
            print("**********************下载完成检测完毕*************************************")
            device_msg["android_page"].screen_keep_on()
            device_msg["android_page"].confirm_received_alert(upgrade_tips)
            lock.acquire()
            ota_page.go_to_new_address("ota/log")
            now_time = ota_page.get_current_time()
            while True:
                info = ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                if len(info) != 0:
                    action = info[0]["Action"]
                    print("action", action)
                    if ota_page.get_action_status(action) == 4:
                        break
                # wait upgrade 30 min at most
                if ota_page.get_current_time() > ota_page.return_end_time(now_time, 1800):
                    assert False, "@@@@30分钟还没有升级相应的安卓版本， 请检查！！！"
                ota_page.time_sleep(5)
                ota_page.refresh_page()
            lock.release()
            print("***************************************设备%s ota升级上报完成*********************************" % device_msg[
                "ip"])

            device_msg["android_page"].device_boot(device_msg["ip"])
            after_upgrade_version = device_msg["android_page"].check_firmware_version()
            assert ota_page.transfer_version_into_int(
                device_current_firmware_version) != ota_page.transfer_version_into_int(after_upgrade_version), \
                "@@@@ota升级失败， 还是原来的版本%s！！" % device_current_firmware_version
            assert ota_page.transfer_version_into_int(release_info["version"]) == \
                   ota_page.transfer_version_into_int(
                       after_upgrade_version), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
            print("***************************************设备%s ota 检测完成*********************************" % device_msg[
                "ip"])

        #
        # multi threads upgrade ota package
        upgrade_threads = []
        for upgrade_i in range(len(devices_data)):
            ota_msg = {"android_page": st.AndroidAimdmPageWiFi(devices_data[upgrade_i], 5), "sn": devices_sn[upgrade_i],
                       "ip": devices_ip[upgrade_i], "package_name": release_info["package_name"],
                       "version": release_info["version"]}
            upgrade_t = st.threading.Thread(target=check_devices_upgrade_ota_package, args=(ota_msg,))
            upgrade_t.start()
            upgrade_threads.append(upgrade_t)
        for upgrade_thread in upgrade_threads:
            upgrade_thread.join()
