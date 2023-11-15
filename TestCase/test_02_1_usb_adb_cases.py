import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()
test_yml = case_pack.yaml_data


class TestNetworkCases:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.APPSPage(self.driver, 40)
        self.ota_page = case_pack.OTAPage(self.driver, 40)
        self.device_page = case_pack.DevicesPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.cat_log_page = case_pack.CatchLogPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.page.delete_app_install_and_uninstall_logs()
        self.ota_page.delete_all_ota_release_log()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.android_mdm_page.device_unlock()

    def teardown_class(self):
        # pass
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        self.page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_usb-test')
    @allure.title("Apps- 断网重连获取aimdm消耗的流量")
    def test_reconnect_get_mobile_data(self, connect_wifi_adb_USB):
        length = 2
        self.android_mdm_page.confirm_wifi_btn_close()
        self.android_mdm_page.disconnect_ip(self.device_sn)
        self.android_mdm_page.open_mobile_data()
        now_time = self.android_mdm_page.get_current_time()
        while True:
            try:
                if self.android_mdm_page.ping_network():
                    break
            except AssertionError:
                pass
            self.android_mdm_page.open_mobile_data()
            if now_time > self.device_page.return_end_time(now_time, 90):
                assert False, "@@@@@无法开启移动网络， 请检查！！！！"
            self.device_page.time_sleep(1)
        opt_case.check_single_device(self.device_sn)
        base_directory = "Mobile_Data_Used"
        first_data_used = 0
        last_data_used = 0
        for i in range(length):
            # self.android_mdm_page.open_mobile_data()
            self.android_mdm_page.screen_keep_on_USB()
            # clear all app data before testing
            self.android_mdm_page.clear_recent_app_USB()
            data_used = self.android_mdm_page.get_aimdm_mobile_data()
            if i == 0:
                first_data_used = data_used
            image_before_disconnect = "%s\\data_used_disconnect_network_%d.jpg" % (base_directory, i)
            self.android_mdm_page.save_screenshot_to_USB(image_before_disconnect)
            self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_before_disconnect,
                                                   "data_used_disconnect_network_%d" % i)
            print("第%d次断网前的使用数据详情： %s" % (i, data_used))
            log.info("第%d次断网前前的使用数据详情： %s" % (i, data_used))
            self.android_mdm_page.clear_recent_app_USB()
            self.android_mdm_page.time_sleep(2)
            self.android_mdm_page.close_mobile_data()

            now_time = self.android_mdm_page.get_current_time()
            while True:
                try:
                    if self.android_mdm_page.no_network():
                        break
                except AssertionError:
                    pass
                self.android_mdm_page.close_mobile_data()
                if now_time > self.device_page.return_end_time(now_time, 90):
                    assert False, "@@@@@无法关闭移动网络， 请检查！！！！"
                self.device_page.time_sleep(1)
            # not stable
            # status = opt_case.get_single_device_list(self.device_sn)[0]
            self.android_mdm_page.time_sleep(10)
            self.android_mdm_page.open_mobile_data()
            self.android_mdm_page.screen_keep_on_USB()
            now_time = self.android_mdm_page.get_current_time()
            while True:
                try:
                    if self.android_mdm_page.ping_network():
                        break
                except AssertionError:
                    pass
                self.android_mdm_page.open_mobile_data()
                if now_time > self.device_page.return_end_time(now_time, 90):
                    assert False, "@@@@@无法开启移动网络， 请检查！！！！"
                self.device_page.time_sleep(1)
            # not stable
            # opt_case.check_single_device(self.device_sn)
            # status = opt_case.get_single_device_list(self.device_sn)[0]
            self.android_mdm_page.clear_recent_app_USB()
            data_used_reconnect = self.android_mdm_page.get_aimdm_mobile_data()
            if i == length - 1:
                last_data_used = data_used_reconnect
            image_after_connect = "%s\\data_used_reconnect_network_%d.jpg" % (base_directory, i)
            self.android_mdm_page.save_screenshot_to_USB(image_after_connect)
            self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_after_connect,
                                                   "data_used_reconnect_network_%d" % i)
            print("第%d次重连后的使用数据详情： %s" % (i, data_used_reconnect))
            log.info("第%d次重连后的使用数据详情： %s" % (i, data_used_reconnect))
        first_data_float = self.device_page.remove_space(self.device_page.extract_integers(first_data_used)[0])
        last_data_float = self.device_page.remove_space(self.device_page.extract_integers(last_data_used)[0])
        total_data_used = float(last_data_float) - float(first_data_float)

        print("总共使用了流量数据： %s MB" % str(round(total_data_used, 2)))
        log.info("总共使用了流量数据： %s MB" % str(round(total_data_used, 2)))
        self.android_mdm_page.clear_recent_app_USB()
        self.android_mdm_page.open_wifi_btn()
        self.android_mdm_page.confirm_wifi_status_open()

    @allure.feature('MDM_usb-test')
    @allure.title("Apps-限定4G网络推送app")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_limit_4G(self, connect_wifi_adb_USB, del_all_app_release_log,
                                  del_all_app_uninstall_release_log,
                                  uninstall_multi_apps, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "Sim Card"}
        # release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
        #                 "silent": "Yes", "network": "Wifi/Ethernet"
        log.info("***********************************限定4G网络推送app用例开始**************************************")
        print("***********************************限定4G网络推送app用例开始**************************************")
        log.info("准备连接wifi")
        print("准备连接wifi")
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        log.info("成功连接wifi")
        print("准备连接wifi")
        # file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        file_path = self.page.get_apk_path(release_info["package_name"])
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])

        # check app size(bytes) in windows
        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        log.info("获取到 app的size: %s" % app_size)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(8)
        # go to app page
        self.page.go_to_new_address("apps")

        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            err_msg = "没有相应的升级包 %s, 请检查！！！" % release_info["package_name"]
            log.error(err_msg)
            print(err_msg)
            assert False, err_msg
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        log.info("推送app： %s" % release_info["package_name"])
        # go to app release log
        # self.page.go_to_new_address("apps/releases")
        # # self.page.check_release_log_info(send_time, release_info["sn"])
        #
        # now_time = self.page.get_current_time()
        # # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        # while True:
        #     release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
        #     else:
        #         self.page.refresh_page()
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app release log， 请检查！！！"
        #     self.page.time_sleep(3)

        # check if no upgrade log in wifi network environment
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        now_time = self.page.get_current_time()
        while True:
            if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                err_msg = "@@@@在非4G网络可以下载app， 请检查！！！！"
                log.error(err_msg)
                assert False, err_msg
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                break

        log.info("在非4G网络1分钟没检测到有下载记录")

        # disconnect wifi
        self.android_mdm_page.disconnect_ip(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_btn_close()
        log.info("成功断开wifi")
        self.page.time_sleep(3)
        log.info("打开流量数据")
        self.android_mdm_page.open_mobile_data()
        log.info("成功过打开流量数据")
        # check if app download in 4G environment
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print(action)
        #         if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
        #                 or self.page.get_action_status(action) == 3:
        #             # check the app size in device, check if app download fully
        #             shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        #             if not self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
        #                 err_msg = "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
        #                 log.error(err_msg)
        #                 assert False, err_msg
        #
        #             size = self.android_mdm_page.get_file_size_in_device_USB(shell_app_apk_name)
        #             print("终端下载后的的size大小：", size)
        #             log.info("终端下载后的的size大小：%s" % size)
        #             if app_size != size:
        #                 print("电脑端下载后的的size大小：%s" % size)
        #                 err_msg = "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #                 log.error(err_msg)
        #                 assert False, err_msg
        #             break
        #     # wait 20 mins
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
        #         err_msg = "@@@@20分钟还没有下载完相应的app， 请检查！！！"
        #         log.error(err_msg)
        #         assert False, err_msg
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        # check if download completed

        # check download record in device
        now_time = self.page.get_current_time()
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
        print("**********************下载记录检测完毕*************************************")

        now_time = self.page.get_current_time()
        original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % release_info["package_name"])
        print("original hash value: %s" % original_hash_value)
        while True:
            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device_USB(shell_app_apk_name)
            print("shell_hash_value: %s" % original_hash_value)
            if original_hash_value == shell_hash_value:
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
            self.page.time_sleep(5)

        log.info("app下载完成")

        # connect wifi
        self.android_mdm_page.open_wifi_btn()
        log.info("打开wifi按钮")
        self.android_mdm_page.confirm_wifi_status_open()
        self.android_mdm_page.connect_ip(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        log.info("连接上wifi adb ")

        # check upgrade
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print("action", action)
        #         if self.page.get_action_status(action) == 4:
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 msg = "成功安装%s" % release_info
        #                 log.info(msg)
        #                 print(msg)
        #                 break
        #             else:
        #                 err_msg = "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
        #                 print(err_msg)
        #                 log.error(err_msg)
        #                 assert False, err_msg
        #     # wait upgrade 3 min at most
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
        #         error_msg = "@@@@3分钟还没有安装完相应的app， 请检查！！！"
        #         print(error_msg)
        #         log.error(error_msg)
        #         assert False, error_msg
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        # self.page.time_sleep(5)
        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                self.page.time_sleep(5)
                self.page.refresh_page()
                upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
                if len(upgrade_list) != 0:
                    action = upgrade_list[0]["Action"]
                    print("action", action)
                    if self.page.get_action_status(action) == 4:
                        break
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)
        self.page.time_sleep(5)
        log.info("***********************************限定4G网络推送app用例运行成功**************************************")
        print("***********************************限定4G网络推送app用例运行成功**************************************")

    @allure.feature('MDM_usb-test')
    @allure.title("Apps-限定WIFI网络推送app")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_limit_wifi(self, connect_wifi_adb_USB, del_all_app_release_log,
                                    del_all_app_uninstall_release_log,
                                    go_to_app_page):
        # release_info = {"package_name": test_yml['app_info']['other_app_limit_network_B'], "sn": self.device_sn,
        #                 "silent": "Yes", "download_network": "Sim Card"}
        log.info("***********************************限定wifi/eth0网络推送app用例开始**************************************")
        print("***********************************限定wifi/eth0网络推送app用例开始**************************************")
        release_info = {"package_name": test_yml['app_info']['other_app_limit_network_B'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "Wifi/Ethernet"}
        log.info("准备断开wifi")
        print("准备断开wifi")
        # disconnect wifi, open data
        self.android_mdm_page.disconnect_ip(self.wifi_ip)
        self.android_mdm_page.close_wifi_btn()
        self.android_mdm_page.confirm_wifi_btn_close()
        log.info("成功断开wifi")
        print("成功断开wifi")
        self.page.time_sleep(3)
        log.info("准备打开流量数据")
        print("准备打开流量数据")
        self.android_mdm_page.open_mobile_data()
        log.info("成功打开流量数据")
        print("成功打开流量数据")

        file_path = self.page.get_apk_path(release_info["package_name"])
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])

        # check app size(bytes) in windows
        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        log.info("电脑端获取到app的size : %s" % str(app_size))
        # go to app page
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(10)
        self.page.go_to_new_address("apps")
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            err_msg = "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
            log.error(err_msg)
            print(err_msg)
            assert False, err_msg
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        # go to app release log
        # self.page.go_to_new_address("apps/releases")
        # self.page.check_release_log_info(send_time, release_info["sn"])

        # now_time = self.page.get_current_time()
        # # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        # while True:
        #     release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
        #     else:
        #         self.page.refresh_page()
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         err_msg = "@@@@没有相应的 app release log， 请检查！！！"
        #         log.error(err_msg)
        #         print(err_msg)
        #         assert False, err_msg
        #     self.page.time_sleep(3)
        # log.info("平台推送app, 并且可检测到推送记录")
        # check if no upgrade log in wifi network environment
        # check the app action in app upgrade logs, if download complete or upgrade complete, break

        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        now_time = self.page.get_current_time()
        while True:
            if self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
                err_msg = "@@@@在非wifi/eth0网络可以下载app， 请检查！！！！"
                log.error(err_msg)
                assert False, err_msg
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                log.info("在wifi/eth0网络1分钟没检测到有下载记录")
                break
        log.info("准备连接wifi/eth0")
        # connect wifi
        self.android_mdm_page.close_mobile_data()
        self.android_mdm_page.open_wifi_btn()
        self.android_mdm_page.confirm_wifi_btn_open()
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        log.info("成功连接到wifi")
        print("成功连接到wifi")

        # check download record in device
        now_time = self.page.get_current_time()
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
        print("**********************下载记录检测完毕*************************************")

        # check if app download in 4G environment
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        log.info("准备检查平台app的下载记录以及终端的下载记录")
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print(action)
        #         if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
        #                 or self.page.get_action_status(action) == 3:
        #             log.info("检测到平台有app下载完成的记录")
        #             # check the app size in device, check if app download fully
        #             shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        #             if not self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
        #                 assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
        #             log.info("检测到终端也有app相应的下载记录")
        #             size = self.android_mdm_page.get_file_size_in_device_USB(shell_app_apk_name)
        #             log.info("终端下载后的的size大小：%s" % str(size))
        #             print("终端下载后的的size大小：%s" % str(size))
        #             if app_size != size:
        #                 err = "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #                 log.error(err)
        #                 assert False, err
        #             break
        #     # wait 20 mins
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
        #         err_msg = "@@@@20分钟还没有下载完相应的app， 请检查！！！"
        #         log.error(err_msg)
        #         print(err_msg)
        #         assert False, err_msg
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        #     log.info("下载完成")
        #     print("下载我弄成")

        # check upgrade
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print("action", action)
        #         if self.page.get_action_status(action) == 4:
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 log.info("成功安装app %s" % release_info["package"])
        #                 print("成功安装app %s" % release_info["package"])
        #                 break
        #             else:
        #                 err_msg = "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
        #                 log.error(err_msg)
        #                 print(err_msg)
        #                 assert False, err_msg
        #     # wait upgrade 3 min at most
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
        #         err_msg = "@@@@3分钟还没有安装完相应的app， 请检查！！！"
        #         log.error(err_msg)
        #         assert False, err_msg
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        # self.page.time_sleep(5)
        now_time = self.page.get_current_time()
        original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % release_info["package_name"])
        print("original hash value: %s" % original_hash_value)
        while True:
            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
            print("shell_hash_value: %s" % original_hash_value)
            if original_hash_value == shell_hash_value:
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
            self.page.time_sleep(5)
        print("终端下载完成")
        log.info("终端下载完成")

        now_time = self.page.get_current_time()
        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                break
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)
        self.page.time_sleep(5)
        print("app终端安装完成")
        log.info("app终端安装完成")

        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(30)

        print("*******************限制wifi网络下载安装完成***************************")
        log.info("*******************限制wifi网络下载安装完成***************************")

    @allure.feature('MDM_usb-test1')
    @allure.title("OTA-OTA断网重连5次断点续传")
    def test_upgrade_OTA_package_reconnect_network_5times(self, connect_wifi_adb_USB, del_all_ota_release_log,
                                                          go_to_ota_page,
                                                          delete_ota_package_relate):
        print("*******************OTA断网重连断点续传用例开始***************************")
        log.info("*******************OTA断网重连断点续传用例开始***************************")
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "category": "NO Limit", "network": "NO Limit"}
        times = 2
        self.android_mdm_page.screen_keep_on()
        self.android_mdm_page.back_to_home()
        # close mobile data first
        log.info("先关闭流量数据")
        self.android_mdm_page.close_mobile_data()
        # get release ota package version
        release_info["version"] = self.page.get_ota_package_version(release_info["package_name"])
        current_firmware_version = self.android_mdm_page.check_firmware_version()
        # compare current version and exp version
        err_info = "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
        assert self.page.transfer_version_into_int(current_firmware_version) < self.page.transfer_version_into_int(
            release_info["version"]), err_info

        device_current_firmware_version = self.android_mdm_page.check_firmware_version()
        print("ota after upgrade version:", release_info["version"])
        log.info("固件升级到版本%s" % release_info["version"])
        # check file size and hash value in directory Param/package
        ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
        act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
        print("act_ota_package_size:", act_ota_package_size)
        log.info("ota升级包的大小: %s" % str(act_ota_package_size))
        # check file hash value in directory Param/package
        act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_ota_package_hash_value)
        log.info("ota升级包的hash值: %s" % str(act_ota_package_hash_value))
        # search package
        self.ota_page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        print("send_time", send_time)
        self.page.time_sleep(8)
        # if device is existed, click
        self.ota_page.click_release_btn()
        # nolimit  simcard  wifiethernet
        self.ota_page.input_release_OTA_package(release_info)
        # self.ota_page.go_to_new_address("ota/release")
        # now_time = self.page.get_current_time()
        # # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        # while True:
        #     release_len = len(self.ota_page.get_ota_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@释放一次ota升级包，有多条释放记录，请检查！！！"
        #     else:
        #         self.ota_page.refresh_page()
        #     if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time):
        #         err_msg = "@@@@没有相应的 ota package release log， 请检查！！！"
        #         print(err_msg)
        #         log.error(err_msg)
        #         assert False, err_msg
        #     self.ota_page.time_sleep(3)

        self.android_mdm_page.screen_keep_on()
        log.info("终端确认下载")
        self.android_mdm_page.confirm_received_alert(download_tips)

        # check download record in device
        now_time = self.page.get_current_time()
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed_USB(release_info["package_name"]):
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]

        log.info("检测到下载记录")

        # check the app action in ota upgrade logs page, if download complete or upgrade complete, break
        # self.ota_page.go_to_new_address("ota/log")
        # now_time = self.ota_page.get_current_time()
        # while True:
        #     info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
        #     if len(info) != 0:
        #         action = info[0]["Action"]
        #         print("action: ", action)
        #         check_file_time = self.ota_page.get_current_time()
        #         if self.ota_page.get_action_status(action) == 1:
        #             log.info("平台显示正在下载中")
        #             while True:
        #                 if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
        #                     log.info("终端检测到相应的下载记录")
        #                     break
        #                 if self.ota_page.get_current_time() > self.ota_page.return_end_time(check_file_time, 60):
        #                     e_msg = "@@@@平台显示正在下载ota升级包， 1分钟在终端检车不到升级包， 请检查！！！"
        #                     log.error(e_msg)
        #                     print(e_msg)
        #                     assert False, e_msg
        #                 self.ota_page.time_sleep(2)
        #             break
        #     if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
        #         err_m = "@@@@3分钟还没有检查到平台有相应的ota package下载记录， 请检查！！！"
        #         log.error(err_m)
        #         print(err_m)
        #         assert False, err_m
        #     self.ota_page.time_sleep(5)

        package_size = self.android_mdm_page.get_file_size_in_device_USB(release_info["package_name"])
        print("断网前下载的的ota package size: ", package_size)
        log.info("断网前下载的的ota package size: %s" % str(package_size))
        for i in range(times):
            self.android_mdm_page.disconnect_ip(self.wifi_ip)
            self.android_mdm_page.close_wifi_btn()
            self.android_mdm_page.confirm_wifi_btn_close()
            self.android_mdm_page.no_network()
            self.page.time_sleep(5)
            self.android_mdm_page.open_wifi_btn()
            self.android_mdm_page.confirm_wifi_btn_open()
            self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
            self.android_mdm_page.ping_network()
            # need to release again, skip below steps
            # self.ota_page.go_to_new_address("ota/release")
            # self.ota_page.select_release_log()
            # self.ota_page.release_again()
            # try:
            #     self.android_mdm_page.confirm_received_alert(download_tips)
            # except Exception:
            #     assert False, "@@@@断网重连后一段时间内没有接受到下载的提示， 请检查！！！！"
            # now_time = self.ota_page.get_current_time()
            while True:
                current_size = self.android_mdm_page.get_file_size_in_device_USB(release_info["package_name"])
                print("断网%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                log.info("断网%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                if current_size == act_ota_package_hash_value:
                    err_info = "@@@@请检查ota 升级包大小是否适合！！！！"
                    print(err_info)
                    assert False, err_info
                if current_size > package_size:
                    package_size = current_size
                    break
                if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                    err_msg = "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载， 请检查！！！"
                    print(err_msg)
                    log.error(err_msg)
                    assert False, err_msg
                self.ota_page.time_sleep(3)

        print("*******************完成%d次断网操作*********************************" % times)

        now_time = self.ota_page.get_current_time()
        while True:
            download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
            package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
            if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
                print("原来升级包的 package_hash_value：", package_hash_value)
                print("下载完成后的 package_hash_value：", package_hash_value)
                log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
                log.info("下载完成后的 package_hash_value：%s" % str(package_hash_value))
                break

            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 420):
                err_msg = "@@@@断网重连%d次， 50分钟后还没有下载完相应的ota package， 请检查！！！" % times
                log.error(err_msg)
                print(err_msg)
                assert False, err_msg
            self.ota_page.time_sleep(10)

        self.ota_page.go_to_new_address("ota/log")
        now_time = self.ota_page.get_current_time()
        while True:
            info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action: ", action)
                if self.ota_page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    break
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                err_msg = "@@@@终端下载完升级包后， 平台3分钟还没有下载完相应的ota package， 请检查！！！"
                log.error(err_msg)
                print(err_msg)
                assert False, err_msg
            self.ota_page.time_sleep(30)
            self.ota_page.refresh_page()
        print("===============================ota升级升级包下载完成============================================")
        log.info("===============================ota升级升级包下载完成============================================")
        self.android_mdm_page.screen_keep_on()
        self.android_mdm_page.confirm_alert_show()
        log.info("检测到有升级提示框")
        try:
            self.android_mdm_page.click_cancel_btn()
        except Exception as e:
            pass
        print("*******************OTA断网重连断点续传用例结束***************************")
        log.info("*******************OTA断网重连断点续传用例结束***************************")

    @allure.feature('MDM_usb-test')
    @allure.title("public case- 设备下线无法发送捕捉日志命令")
    def test_fail_to_catch_log_when_offline(self, go_to_device_page, connect_wifi_adb_USB):
        print("*******************设备下线无法发送捕捉日志命令***************************")
        log.info("*******************设备下线无法发送捕捉日志命令***************************")
        self.android_mdm_page.disconnect_ip(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_btn_close()
        self.android_mdm_page.close_mobile_data()
        self.android_mdm_page.no_network()
        self.page.time_sleep(120)
        self.device_page.refresh_page()
        device_msg = opt_case.get_single_device_list(self.device_sn)[0]
        assert "Off" in device_msg["Status"], "@@@设备网络已经关掉， 平台显示设备还在线， 请检查！！！"
        self.device_page.select_device(self.device_sn)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(case_pack.time.time()))
        self.device_page.click_dropdown_btn()

        self.device_page.click_cat_log()
        self.device_page.show_log_type()
        self.device_page.select_app_log()
        self.device_page.click_save_catch_log_fail()
        self.device_page.refresh_page()
        self.page.go_to_new_address("catchlog/task")
        now_time = self.page.get_current_time()
        while True:
            if len(self.cat_log_page.get_latest_catch_log_list(send_time, self.device_sn)) >= 1:
                assert False, "@@@@设备不在线，不应该有相应的catch log！！！"
            else:
                self.page.refresh_page()
            # wait 20 min
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                break
            self.page.time_sleep(5)

        print("*******************设备下线无法发送捕捉日志命令用例结束***************************")
        log.info("*******************设备下线无法发送捕捉日志命令用例结束***************************")

    @allure.feature('MDM_usb-test')
    @allure.title("Apps-推送低版本的APP")
    @pytest.mark.dependency(name="test_release_app_ok", scope='package')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_low_version_app(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['low_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        # apk_info = {"package_name": "ComAssistant.apk", "sn": "A250900P03100019",
        #                 "silent": "Yes", "version": "1.1"}

        # release_info = {"package_name": "ComAssistant.apk", "sn": "A250900P03100019",
        #                 "silent": "Yes"}
        file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])

        # check if the app is existed, if existed, uninstall, else push
        # if self.android_mdm_page.app_is_installed(release_info["package"]):
        #     self.android_mdm_page.uninstall_app(release_info["package"])

        # app_size_mdm = self.page.get_app_size()  for web
        # check app size(bytes) in windows
        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        # self.android_mdm_page.start_app()
        # go to app page
        self.page.go_to_new_address("apps")
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(4)
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        # go to app release log
        # self.page.go_to_new_address("apps/releases")
        # self.page.check_release_log_info(send_time, release_info["sn"])

        # now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        # while True:
        #     release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
        #     else:
        #         self.page.refresh_page()
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app release log， 请检查！！！"
        #     self.page.time_sleep(3)

        # check if the upgrade log appeared, if appeared, break
        # self.page.go_to_new_address("apps/logs")
        # now_time = self.page.get_current_time()
        # while True:
        #     release_len = len(self.page.get_app_latest_upgrade_log(send_time, release_info))
        #     if release_len == 1:
        #         break
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()

        # check the app download record in device

        # check download record in device
        now_time = self.page.get_current_time()
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
        print("**********************下载记录检测完毕*************************************")

        # check if download completed
        now_time = self.page.get_current_time()
        original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % release_info["package_name"])
        print("original hash value: %s" % original_hash_value)
        while True:
            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
            print("shell_hash_value: %s" % original_hash_value)
            if original_hash_value == shell_hash_value:
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
            self.page.time_sleep(5)
        print("**********************下载完成检测完毕*************************************")

        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print(action)
        #         if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
        #                 or self.page.get_action_status(action) == 3:
        #             # check the app size in device, check if app download fully
        #             shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        #             if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
        #                 assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
        #
        #             size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
        #             print("终端下载后的的size大小：", size)
        #             if app_size != size:
        #                 assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #             print("=============下载完成")
        #             break
        #     # wait 20 mins
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
        #         assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        #

        # # check install

        # check upgrade
        now_time = self.page.get_current_time()
        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(1)
        print("**********************终端安装完毕*************************************")

        self.page.time_sleep(5)

        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(30)
            self.page.refresh_page()
        self.page.time_sleep(5)

        # # check upgrade
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print("action", action)
        #         if self.page.get_action_status(action) == 4:
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 break
        #             else:
        #                 assert False, "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
        #     # wait upgrade 3 mins at most
        #     print("=======在这里11111")
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
        #         assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        # self.page.time_sleep(5)
        print("*******************静默安装完成***************************")
        log.info("*******************静默安装完成***************************")

        send_time_final = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                  case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(4)
        # uninstall app and check if app would be installed again in 10min
        self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
        # disconnect wifi
        self.android_mdm_page.disconnect_ip(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_btn_close()
        self.page.time_sleep(3)
        self.android_mdm_page.open_mobile_data()
        self.android_mdm_page.confirm_wifi_btn_open()
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        # check upgrade
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time_final, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print(" upgrade action:", action)
        #         if self.page.get_action_status(action) == 4:
        #             print("******************************************")
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 version_installed = self.page.transfer_version_into_int(
        #                     self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
        #                 if version_installed == self.page.transfer_version_into_int(release_info["version"]):
        #                     break
        #                 else:
        #                     assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
        #     # wait upgrade 3 mins at most
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 610):
        #         log.error("@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！")
        #         assert False, "@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！"
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        now_time = self.page.get_current_time()
        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有终端没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(1)
        self.page.time_sleep(5)

        self.page.refresh_page()
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time_final, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(30)
            self.page.refresh_page()
        log.info("*******************卸载后重新安装成功***************************")
        print("*******************卸载后重新安装成功***************************")

    @allure.feature('MDM_usb-test')
    @allure.title("Apps-推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装")
    @pytest.mark.dependency(depends=["test_release_app_ok"], scope='package')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_high_version_app_cover_low_version_app(self, del_all_app_release_log, del_all_app_uninstall_release_log,
                                                    go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}

        file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # app_size_mdm = self.page.get_app_size()  for web
        # check app size(bytes) in windows
        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)

        # go to app page
        self.page.go_to_new_address("apps")
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(8)
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        # go to app release log
        # self.page.go_to_new_address("apps/releases")
        # self.page.check_release_log_info(send_time, release_info["sn"])

        # now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        # while True:
        #     release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app release log， 请检查！！！"
        #     self.page.time_sleep(1)
        #     self.page.refresh_page()

        # check if the upgrade log appeared, if appeared, break

        # check release record in device

        now_time = self.page.get_current_time()
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
        print("**********************下载记录检测完毕*************************************")

        # check if download completed
        now_time = self.page.get_current_time()
        original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % release_info["package_name"])
        print("original hash value: %s" % original_hash_value)
        while True:
            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
            print("shell_hash_value: %s" % original_hash_value)
            if original_hash_value == shell_hash_value:
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
            self.page.time_sleep(60)
        print("**********************下载完成检测完毕*************************************")

        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                version_installed = self.page.transfer_version_into_int(
                    self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                if version_installed == self.page.transfer_version_into_int(release_info["version"]):
                    break
                else:
                    assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(1)
        self.page.time_sleep(5)
        print("**********************终端成功安装app*************************************")

        self.page.go_to_new_address("apps/logs")
        self.page.refresh_page()
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(60)
            self.page.refresh_page()
        self.page.time_sleep(5)

        # self.page.go_to_new_address("apps/logs")
        # now_time = self.page.get_current_time()
        # while True:
        #     release_len = len(self.page.get_app_latest_upgrade_log(send_time, release_info))
        #     if release_len == 1:
        #         break
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
        #     self.page.time_sleep(3)
        #     self.page.refresh_page()

        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
        #                 or self.page.get_action_status(action) == 3:
        #             # check the app size in device, check if app download fully
        #             shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        #             if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
        #                 assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
        #
        #             size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
        #             print("终端下载后的的size大小：", size)
        #             if app_size != size:
        #                 assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #             break
        #         # wait 20 mins
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 1200):
        #         assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
        #     self.page.refresh_page()
        #     self.page.time_sleep(5)

        # check upgrade
        # now_time = self.page.get_current_time()
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print("action", action)
        #         if self.page.get_action_status(action) == 4:
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 version_installed = self.page.transfer_version_into_int(
        #                     self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
        #                 if version_installed == self.page.transfer_version_into_int(release_info["version"]):
        #                     break
        #                 else:
        #                     assert False, "@@@@平台显示已经完成覆盖安装了app, 终端发现没有安装高版本的app，还是原来的版本， 请检查！！！！"
        #     # wait upgrade 3 mins at most
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
        #         assert False, "@@@@3分钟还没有静默安装完相应的app， 请检查！！！"
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        # self.page.time_sleep(5)
        print("*******************静默覆盖安装完成***************************")
        log.info("*******************静默覆盖安装完成***************************")
        # uninstall app and reboot, check if app would be reinstalled again
        now_time = self.page.get_current_time()
        send_time_again = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                  case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(5)
        self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
        self.android_mdm_page.reboot_device(self.wifi_ip)

        # check upgrade
        # while True:
        #     upgrade_list = self.page.get_app_latest_upgrade_log(send_time_again, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print("action", action)
        #         if self.page.get_action_status(action) == 4:
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 version_installed_again = self.page.transfer_version_into_int(
        #                     self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
        #                 if version_installed_again == self.page.transfer_version_into_int(release_info["version"]):
        #                     break
        #                 else:
        #                     assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
        #     # wait upgrade 3 mins at most
        #     if self.page.get_current_time() > self.page.return_end_time(now_time, 610):
        #         log.error("@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！")
        #         assert False, "@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！"
        #     self.page.time_sleep(5)
        #     self.page.refresh_page()
        # self.page.time_sleep(5)
        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                version_installed = self.page.transfer_version_into_int(
                    self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                if version_installed == self.page.transfer_version_into_int(release_info["version"]):
                    break
                else:
                    assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(1)
        self.page.time_sleep(5)
        print("**********************终端成功安装app*************************************")

        self.page.refresh_page()
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time_again, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                break
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
            self.page.time_sleep(60)
            self.page.refresh_page()
        self.page.time_sleep(5)
        log.info("*******************卸载并重启后重新安装成功***************************")
        print("*******************卸载并重启后重新安装成功***************************")

    @allure.feature('MDM_usb-test')
    @allure.title("public case-有线休眠推送app")
    def test_report_device_sleep_status_usb(self, del_all_app_release_log,
                                            del_all_app_uninstall_release_log, go_to_device_page, connected_wifi_adb):
        print("*******************有线休眠推送app用例开始***************************")
        log.info("*******************有线休眠推送app用例开始***************************")
        # self.android_mdm_page.confirm_wifi_status_open()
        # self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        self.android_mdm_page.screen_keep_on()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.back_to_home()
        # self.android_mdm_page.confirm_unplug_usb_wire()

        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        file_path = self.page.get_apk_path(release_info["package_name"])
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version

        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        # check file hash value in directory Param/package
        act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_apk_package_hash_value)

        device_info = opt_case.check_single_device(self.device_sn)[0]
        msg = "online"
        # clear other alert
        if self.device_page.upper_transfer("on") in self.device_page.remove_space_and_upper(device_info["Status"]):
            if self.device_page.upper_transfer("Locked") in self.device_page.remove_space_and_upper(
                    device_info["Lock Status"]):
                self.device_page.select_device(self.device_sn)
                self.device_page.click_unlock()
        if self.android_mdm_page.public_alert_show(2):
            self.android_mdm_page.clear_download_and_upgrade_alert()

        self.device_page.select_device(self.device_sn)
        self.device_page.send_message(msg)
        if not self.android_mdm_page.public_alert_show(60):
            assert False, "@@@@平台显示设备在线， 发送消息一分钟后还没收到消息"
        self.android_mdm_page.confirm_received_text(msg, timeout=5)
        try:
            self.android_mdm_page.click_msg_confirm_btn()
            self.android_mdm_page.confirm_msg_alert_fade(msg)
        except Exception:
            pass

        self.android_mdm_page.device_sleep()
        # self.android_mdm_page.time_sleep(60)
        self.android_mdm_page.time_sleep(test_yml["android_device_info"]["sleep_time"])
        log.info("设备进入休眠状态")
        print("设备进入休眠状态")
        self.device_page.refresh_page()
        opt_case.check_single_device(self.device_sn)
        self.android_mdm_page.device_is_existed(self.wifi_ip)
        # self.device_page.select_device(self.device_sn)
        # self.device_page.send_message(msg)
        # if not self.android_mdm_page.public_alert_show(60):
        #     assert False, "@@@@平台显示设备在线， 发送消息一分钟后还没收到消息"
        # self.android_mdm_page.confirm_received_text(msg, timeout=5)
        # try:
        #     self.android_mdm_page.click_msg_confirm_btn()
        #     self.android_mdm_page.confirm_msg_alert_fade(msg)
        # except Exception:
        #     pass

        # go to app page
        self.page.go_to_new_address("apps")
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(4)
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        # go to app release log
        self.page.go_to_new_address("apps/releases")

        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app release log， 请检查！！！"
            self.page.time_sleep(3)

        # check if the upgrade log appeared, if appeared, break
        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            release_len = len(self.page.get_app_latest_upgrade_log(send_time, release_info))
            if release_len == 1:
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
            self.page.time_sleep(5)
            self.page.refresh_page()

        """
        Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
         4: upgrading complete, 5: downloading failed, 6: upgrading failed)
         0: Uninstall completed
        """
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print(action)
                if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    # check the app size in device, check if app download fully
                    shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                    if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
                    size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
                    print("终端下载后的的size大小：", size)
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    print("原来升级包的 package_hash_value：", act_apk_package_hash_value)
                    print("下载完成后的 package_hash_value：", package_hash_value)
                    assert app_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                    assert package_hash_value == act_apk_package_hash_value, "@@@@平台显示下载完成，终端的apk和原始的apkSHA-256值不一致， 请检查！！！！"
                    break
            # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@30分钟还没有下载完相应的app， 请检查！！！"
            self.page.time_sleep(5)
            self.page.refresh_page()

        # check upgrade
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    else:
                        assert False, "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
            # wait upgrade 3 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)
            self.page.refresh_page()
        self.page.time_sleep(5)
        print("*******************有线休眠推送app用例结束***************************")
        log.info("*******************有线休眠推送app用例结束***************************")
