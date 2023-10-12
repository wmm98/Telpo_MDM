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
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.device_sn = self.android_mdm_page.get_device_sn()

    def teardown_class(self):
        self.page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.page.refresh_page()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_network-test')
    @allure.title("Apps-限定4G网络推送app")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_limit_4G(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "Sim Card"}
        # release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
        #                 "silent": "Yes", "network": "Wifi/Ethernet"

        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)

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
        self.page.go_to_new_address("apps/releases")
        # self.page.check_release_log_info(send_time, release_info["sn"])

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

        # check if no upgrade log in wifi network environment
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                assert False, "@@@@在非4G网络下可以下载app， 请检查！！！！"
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                break
            self.page.time_sleep(5)
            self.page.refresh_page()

        # disconnect wifi
        self.android_mdm_page.disconnect_ip(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_btn_close()
        self.page.time_sleep(3)
        self.android_mdm_page.open_mobile_data()

        # check if app download in 4G environment
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
                    if not self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
                        assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"

                    size = self.android_mdm_page.get_file_size_in_device_USB(shell_app_apk_name)
                    print("终端下载后的的size大小：", size)
                    if app_size != size:
                        assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                    break
            # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
            self.page.time_sleep(5)
            self.page.refresh_page()

        # connect wifi
        self.android_mdm_page.open_wifi_btn()
        self.android_mdm_page.confirm_wifi_status_open()
        self.android_mdm_page.connect_ip(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)

        """
                Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
                 4: upgrading complete, 5: downloading failed, 6: upgrading failed)
                 0: Uninstall completed
                """
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
        print("*******************限制4G网络下载安装完成***************************")
        log.info("*******************限制4G网络下载安装完成***************************")

    @allure.feature('MDM_APP-test')
    @allure.title("Apps-限定WIFI网络推送app")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_limit_wifi(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page):
        # release_info = {"package_name": test_yml['app_info']['other_app_limit_network_B'], "sn": self.device_sn,
        #                 "silent": "Yes", "download_network": "Sim Card"}
        release_info = {"package_name": test_yml['app_info']['other_app_limit_network_B'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "Wifi/Ethernet"}

        # disconnect wifi, open data
        self.android_mdm_page.disconnect_ip(self.wifi_ip)
        self.android_mdm_page.close_wifi_btn()
        self.android_mdm_page.confirm_wifi_btn_close()
        self.page.time_sleep(3)
        self.android_mdm_page.open_mobile_data()

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
        # self.page.check_release_log_info(send_time, release_info["sn"])

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

        # check if no upgrade log in wifi network environment
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                assert False, "@@@@在非wifi/eth0网络下可以下载app， 请检查！！！！"
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                break
            self.page.time_sleep(5)
            self.page.refresh_page()

        # connect wifi
        self.android_mdm_page.close_mobile_data()
        self.android_mdm_page.open_wifi_btn()
        self.android_mdm_page.confirm_wifi_btn_open()
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)

        # check if app download in 4G environment
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
                    if not self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
                        assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"

                    size = self.android_mdm_page.get_file_size_in_device_USB(shell_app_apk_name)
                    print("终端下载后的的size大小：", size)
                    if app_size != size:
                        assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                    break
            # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
            self.page.time_sleep(5)
            self.page.refresh_page()

        """
                Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
                 4: upgrading complete, 5: downloading failed, 6: upgrading failed)
                 0: Uninstall completed
                """
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
        print("*******************限制wifi网络下载安装完成***************************")
        log.info("*******************限制wifi网络下载安装完成***************************")

