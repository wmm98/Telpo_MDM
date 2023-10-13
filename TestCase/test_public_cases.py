import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
test_yml = case_pack.yaml_data
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()

log = case_pack.MyLog()

package_infos = [{"package_name": test_yml['app_info']['low_version_app'], "file_category": "test",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['high_version_app'], "file_category": "test",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app'], "file_category": "test01",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app_limit_network_A'], "file_category": "test01",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app_limit_network_B'], "file_category": "test01",
                  "developer": "engineer", "description": "test"}
                 ]


class TestAppPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.app_page = case_pack.APPSPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.app_page.go_to_new_address("apps")

    def teardown_class(self):
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.app_page.refresh_page()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_public-test-test')
    @allure.title("public case-应用满屏推送")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_full_screen(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        file_path = self.app_page.get_apk_path(release_info["package_name"])
        package = self.app_page.get_apk_package_name(file_path)
        release_info["package"] = package
        print("包名：", package)
        version = self.app_page.get_apk_package_version(file_path)
        release_info["version"] = version

        self.android_mdm_page.uninstall_app(release_info["package"])
        self.android_mdm_page.reboot_device(self.wifi_ip)
        # check if device is online
        self.app_page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])

        app_size = self.app_page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        # check file hash value in directory Param/package
        act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_apk_package_hash_value)
        # go to app page
        self.app_page.go_to_new_address("apps")
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.app_page.get_current_time()))
        self.app_page.time_sleep(4)
        self.app_page.search_app_by_name(release_info["package_name"])
        app_list = self.app_page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.app_page.click_release_app_btn()
        self.app_page.input_release_app_info(release_info, kiosk_mode=True)
        # go to app release log
        self.app_page.go_to_new_address("apps/releases")

        now_time = self.app_page.get_current_time()
        # print(self.app_page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.app_page.get_app_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.app_page.refresh_page()
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app release log， 请检查！！！"
            self.app_page.time_sleep(3)

        # check if the upgrade log appeared, if appeared, break
        self.app_page.go_to_new_address("apps/logs")
        now_time = self.app_page.get_current_time()
        while True:
            release_len = len(self.app_page.get_app_latest_upgrade_log(send_time, release_info))
            if release_len == 1:
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
            self.app_page.time_sleep(5)
            self.app_page.refresh_page()

        """
        Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
         4: upgrading complete, 5: downloading failed, 6: upgrading failed)
         0: Uninstall completed
        """
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        now_time = self.app_page.get_current_time()
        while True:
            upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print(action)
                if self.app_page.get_action_status(action) == 2 or self.app_page.get_action_status(action) == 4 \
                        or self.app_page.get_action_status(action) == 3:
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
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                assert False, "@@@@30分钟还没有下载完相应的app， 请检查！！！"
            self.app_page.time_sleep(5)
            self.app_page.refresh_page()

        # check upgrade
        now_time = self.app_page.get_current_time()
        while True:
            upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.app_page.get_action_status(action) == 4:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    else:
                        assert False, "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
            # wait upgrade 3 min at most
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
            self.app_page.time_sleep(5)
            self.app_page.refresh_page()
        self.app_page.time_sleep(5)
        print("*******************静默安装完成***************************")
        log.info("*******************静默安装完成***************************")

        self.android_mdm_page.confirm_app_is_running(release_info["package"])
        base_directory = "APP_Full_Screen"
        image_before_reboot = "%s\\APP满屏推送效果图(重启前).jpg" % base_directory
        self.android_mdm_page.save_screenshot_to(image_before_reboot)
        self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_before_reboot, "APP满屏推送效果图(重启前)")
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.confirm_app_start(release_info["package"])
        image_after_reboot = "%s\\APP满屏推送效果图(重启后).jpg" % base_directory
        self.android_mdm_page.confirm_app_is_running(release_info["package"])
        self.android_mdm_page.save_screenshot_to(image_after_reboot)
        self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_after_reboot, "APP满屏推送效果图(重启后)")
        self.android_mdm_page.stop_app(release_info["package"])
        assert False,  "@@@请在报告查看app满屏效果截图"


