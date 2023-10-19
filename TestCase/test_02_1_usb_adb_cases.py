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
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.android_mdm_page.device_unlock()

    def teardown_class(self):
        self.android_mdm_page.open_wifi_btn()
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        self.page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
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

    @allure.feature('MDM_APP-test-test')
    @allure.title("OTA-OTA断网重连5次断点续传")
    def test_upgrade_OTA_package_reconnect_network_5times(self, del_all_ota_release_log, go_to_ota_page,
                                                          delete_ota_package_relate):
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        # close mobile data first
        self.android_mdm_page.close_mobile_data()
        # get release ota package version
        release_info["version"] = self.page.get_ota_package_version(release_info["package_name"])
        current_firmware_version = self.android_mdm_page.check_firmware_version()
        # compare current version and exp version
        assert self.page.transfer_version_into_int(current_firmware_version) < self.page.transfer_version_into_int(
            release_info["version"]), \
            "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
        device_current_firmware_version = self.android_mdm_page.check_firmware_version()
        print("ota after upgrade version:", release_info["version"])
        # check file size and hash value in directory Param/package
        ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
        act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
        print("act_ota_package_size:", act_ota_package_size)
        # check file hash value in directory Param/package
        act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_ota_package_hash_value)
        # search package
        self.ota_page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        print("send_time", send_time)
        self.page.time_sleep(4)
        # if device is existed, click
        self.ota_page.click_release_btn()
        self.ota_page.input_release_OTA_package(release_info)
        self.ota_page.go_to_new_address("ota/release")
        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.ota_page.get_ota_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.ota_page.refresh_page()
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time):
                assert False, "@@@@没有相应的 ota package release log， 请检查！！！"
            self.ota_page.time_sleep(1)

        self.android_mdm_page.confirm_received_alert(download_tips)
        # check the app action in ota upgrade logs page, if download complete or upgrade complete, break
        self.ota_page.go_to_new_address("ota/log")
        now_time = self.ota_page.get_current_time()
        while True:
            info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action: ", action)
                check_file_time = self.ota_page.get_current_time()
                if self.ota_page.get_action_status(action) == 1:
                    while True:
                        if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                            break
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(check_file_time, 60):
                            assert False, "@@@@平台显示正在下载ota升级包， 1分钟在终端检车不到升级包， 请检查！！！"
                        self.ota_page.time_sleep(2)
                    break
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有见检查到相应的ota package下载记录， 请检查！！！"
            self.ota_page.time_sleep(5)

        package_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
        print("断网前下载的的ota package size: ", package_size)
        for i in range(2):
            self.android_mdm_page.disconnect_ip(self.wifi_ip)
            self.android_mdm_page.close_wifi_btn()
            self.android_mdm_page.confirm_wifi_btn_close()
            self.android_mdm_page.no_network()
            self.page.time_sleep(5)
            self.android_mdm_page.open_wifi_btn()
            self.android_mdm_page.confirm_wifi_btn_open()
            self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
            self.android_mdm_page.ping_network()
            # need to release again
            self.ota_page.go_to_new_address("ota/release")
            self.ota_page.select_release_log()
            self.ota_page.release_again()
            try:
                self.android_mdm_page.confirm_received_alert(download_tips)
            except Exception:
                assert False, "@@@@断网重连后一段时间内没有接受到下载的提示， 请检查！！！！"
            now_time = self.ota_page.get_current_time()
            while True:
                current_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                print("断网%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                if current_size == act_ota_package_hash_value:
                    assert False, "@@@@请检查ota 升级包大小是否适合！！！！"
                if current_size > package_size:
                    package_size = current_size
                    break
                if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                    assert False, "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载， 请检查！！！"
                self.ota_page.time_sleep(1)
        print("*******************完成5次断网操作*********************************")
        """
            Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
            4: upgrading complete, 5: downloading failed, 6: upgrading failed)
        """
        self.ota_page.go_to_new_address("ota/log")
        now_time = self.ota_page.get_current_time()
        while True:
            info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action: ", action)
                if self.ota_page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    print("原来升级包的 package_hash_value：", package_hash_value)
                    print("下载完成后的 package_hash_value：", package_hash_value)
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    print("actual_ota_package_size:", act_ota_package_size)
                    print("download_ota_package_size: ", download_file_size)
                    assert act_ota_package_size == download_file_size, "@@@@下载下来的ota包不完整，请检查！！！"
                    assert package_hash_value == act_ota_package_hash_value, "@@@@平台显示下载完成，终端的ota升级包和原始的升级包SHA-256值不一致， 请检查！！！！"
                    break
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 3000):
                assert False, "@@@@断网重连5次， 50分钟后还没有下载完相应的ota package， 请检查！！！"
            self.ota_page.time_sleep(10)
            self.ota_page.refresh_page()
        print("===============================ota升级升级包下载完成============================================")
        self.android_mdm_page.confirm_alert_show()
        self.android_mdm_page.click_cancel_btn()
