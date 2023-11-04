import allure
import TestCase as case_pack
import pytest

conf = case_pack.Config()
test_yml = case_pack.yaml_data
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()


# if test_yml['settings']['test_version']:
#     test_version = 'MDM_test02-no test in test version'

class TestOTAPage:

    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.OTAPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.sn = case_pack.device_data["usb_device_info"]["serial"]
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.android_mdm_page.del_all_downloaded_zip()

    def teardown_class(self):
        self.page.refresh_page()
        self.android_mdm_page.del_all_downloaded_zip()
        self.android_mdm_page.del_updated_zip()

    @allure.feature('MDM_OTA_test02')
    @allure.title("OTA-负责测试用例")
    def test_upgrade_package_page(self, go_to_ota_upgrade_package_page):
        # self.Page.click_OTA_btn()
        # self.Page.click_upgrade_packages()
        self.page.page_load_complete()

    @allure.feature('MDM_test02-no test in test version')
    @allure.title("OTA-Delete OTA package")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_delete_OTA_package(self):
        package_info = {"package_name": test_yml['ota_packages_info']['package_name'], "file_category": "test",
                        "plat_form": test_yml['ota_packages_info']['platform']}
        self.page.refresh_page()
        self.page.search_device_by_pack_name(package_info["package_name"])
        if len(self.page.get_ota_package_list()) == 1:
            self.page.delete_ota_package()
            self.page.refresh_page()
            self.page.search_device_by_pack_name(package_info["package_name"])
            assert len(self.page.get_ota_package_list()) == 0, "@@@@删除失败，请检查！！！"

    @allure.feature('MDM_test02-11122231111')
    @allure.title("OTA-Add OTA package")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_add_OTA_package_and_cate(self, go_to_ota_page):
        exp_existed_text = "ota already existed"
        exp_success_text = "success"
        package_info = {"package_name": test_yml['ota_packages_info']['package_name'], "file_category": "test",
                        "plat_form": test_yml['ota_packages_info']['platform']}
        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        ota_info = {"file_name": file_path, "file_category": package_info["file_category"],
                    "plat_form": package_info["plat_form"]}
        # check if category is existed
        try:
            if len(self.page.get_ota_categories_list()) == 0:
                self.page.add_ota_category("test")
                self.page.refresh_page()
        except Exception as e:
            print(e)
        # check if ota package is existed, if not, add package, else skip
        self.page.search_device_by_pack_name(package_info["package_name"])
        if len(self.page.get_ota_package_list()) == 0:
            self.page.click_add_btn()
            self.page.input_ota_package_info(ota_info)
            self.page.click_save_add_ota_pack()
            self.page.search_device_by_pack_name(package_info["package_name"])
            assert len(self.page.get_ota_package_list()) == 1, "@@@添加失败！！！"

    @allure.feature('MDM_APP-test-test111')
    @allure.title("OTA-OTA重启5次断点续传")
    def test_upgrade_OTA_package_reboot_5times(self, del_all_ota_release_log, go_to_ota_page, delete_ota_package_relate):
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        # get release ota package version
        release_info["version"] = self.page.get_ota_package_version(release_info["package_name"])
        current_firmware_version = self.android_mdm_page.check_firmware_version()
        # compare current version and exp version
        assert self.page.transfer_version_into_int(current_firmware_version) < self.page.transfer_version_into_int(
            release_info["version"]), \
            "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
        # reboot and sync data with platform
        self.android_mdm_page.reboot_device(self.wifi_ip)
        # search package
        device_current_firmware_version = self.android_mdm_page.check_firmware_version()
        print("ota after upgrade version:", release_info["version"])
        # check file size and hash value in directory Param/package
        ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
        act_ota_package_size = self.page.get_zip_size(ota_package_path)
        print("act_ota_package_size:", act_ota_package_size)
        # check file hash value in directory Param/package
        act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_ota_package_hash_value)

        self.page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        print("send_time", send_time)
        self.page.time_sleep(4)
        # if device is existed, click
        self.page.click_release_btn()
        self.page.input_release_OTA_package(release_info)
        self.page.go_to_new_address("ota/release")
        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.page.get_ota_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 ota package release log， 请检查！！！"
            self.page.time_sleep(1)

        self.android_mdm_page.confirm_received_alert(download_tips)
        # check the app action in ota upgrade logs, if download complete or upgrade complete, break
        self.page.go_to_new_address("ota/log")
        now_time = self.page.get_current_time()
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action: ", action)
                check_file_time = self.page.get_current_time()
                if self.page.get_action_status(action) == 1:
                    while True:
                        if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                            break
                        if self.page.get_current_time() > self.page.return_end_time(check_file_time, 60):
                            assert False, "@@@@平台显示正在下载ota升级包， 1分钟在终端检车不到升级包， 请检查！！！"
                        self.page.time_sleep(2)
                    break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有见检查到相应的ota package下载记录， 请检查！！！"
            self.page.time_sleep(5)

        package_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
        print("第一次下载的的ota package size: ", package_size)
        for i in range(5):
            self.android_mdm_page.reboot_device(self.wifi_ip)
            try:
                self.android_mdm_page.confirm_received_alert(download_tips)
            except Exception:
                assert "@@@@开机恢复网络后一段时间内没有接受到下载的提示， 请检查！！！！"
            now_time = self.page.get_current_time()
            while True:
                current_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                print("重启%s次之后当前ota package 的size: %s" % (str(i+1), current_size))
                if current_size == act_ota_package_hash_value:
                    assert False, "@@@@请检查ota 升级包大小是否适合！！！！"
                if current_size > package_size:
                    package_size = current_size
                    break
                if self.page.get_current_time() > self.page.return_end_time(now_time, 120):
                    assert False, "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载"
                self.page.time_sleep(1)
        print("*******************完成5次重启*********************************")

        """
            Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
            4: upgrading complete, 5: downloading failed, 6: upgrading failed)
        """
        now_time = self.page.get_current_time()
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action: ", action)
                if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    print("原来升级包的 package_hash_value：", act_ota_package_hash_value)
                    print("下载完成后的 package_hash_value：", package_hash_value)
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    print("actual_ota_package_size:", act_ota_package_size)
                    print("download_ota_package_size: ", download_file_size)
                    assert act_ota_package_size == download_file_size, "@@@@下载下来的ota包不完整，请检查！！！"
                    assert package_hash_value == act_ota_package_hash_value, "@@@@平台显示下载完成，终端的ota升级包和原始的升级包SHA-256值不一致， 请检查！！！！"
                    break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 3000):
                assert False, "@@@@断点重启5次， 50分钟后还没有下载完相应的ota package， 请检查！！！"
            self.page.time_sleep(10)
            self.page.refresh_page()

        # check upgrade
        self.android_mdm_page.confirm_received_alert(upgrade_tips)
        now_time = self.page.get_current_time()
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    break
            # wait upgrade 30 min at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@30分钟还没有升级相应的安卓版本， 请检查！！！"
            self.page.time_sleep(5)

        self.android_mdm_page.device_boot(self.wifi_ip)
        after_upgrade_version = self.android_mdm_page.check_firmware_version()
        assert self.page.transfer_version_into_int(
            device_current_firmware_version) != self.page.transfer_version_into_int(after_upgrade_version), \
            "@@@@ota升级失败， 还是原来的版本%s！！" % device_current_firmware_version
        assert self.page.transfer_version_into_int(release_info["version"]) == \
               self.page.transfer_version_into_int(
                   after_upgrade_version), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version

    @allure.feature('MDM_OTA_test02')
    @allure.title("OTA-OTA应用推送")
    def test_release_OTA_package_no_limit(self, del_all_ota_release_log, go_to_ota_page):
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        self.android_mdm_page.del_updated_zip()
        release_info["version"] = self.page.get_ota_package_version(release_info["package_name"])
        current_firmware_version = self.android_mdm_page.check_firmware_version()
        # compare current version and exp version
        assert self.page.transfer_version_into_int(current_firmware_version) < self.page.transfer_version_into_int(release_info["version"]),\
            "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"

        # reboot
        self.android_mdm_page.reboot_device(self.wifi_ip)
        # search package

        device_current_firmware_version = self.android_mdm_page.check_firmware_version()
        print("ota after upgrade version:", release_info["version"])
        ota_package_size = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        act_ota_package_size = self.page.get_zip_size(ota_package_size)
        print("act_ota_package_size:", act_ota_package_size)
        self.page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        print("send_time", send_time)
        self.page.time_sleep(4)
        # if device is existed, click
        self.page.click_release_btn()
        self.page.input_release_OTA_package(release_info)
        self.page.go_to_new_address("ota/release")
        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.page.get_ota_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 ota package release log， 请检查！！！"
            self.page.time_sleep(1)

        self.android_mdm_page.confirm_received_alert(download_tips)

        """
                Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
                 4: upgrading complete, 5: downloading failed, 6: upgrading failed)
                """
        # check the app action in ota upgrade logs, if download complete or upgrade complete, break
        self.page.go_to_new_address("ota/log")
        now_time = self.page.get_current_time()
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    break
                else:
                    self.page.refresh_page()
            else:
                self.page.refresh_page()
                # wait 20 min
            if self.page.get_current_time() > self.page.return_end_time(now_time, 2400):
                assert False, "@@@@30分钟还没有下载完相应的ota package， 请检查！！！"
            self.page.time_sleep(5)

        assert self.android_mdm_page.download_file_is_existed(
            release_info["package_name"]), "@@@平台显示已经下载完了升级包， 终端不存在升级包， 请检查！！！"
        download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
        print("actual_ota_package_size:", act_ota_package_size)
        print("download_ota_package_size: ", download_file_size)
        assert act_ota_package_size == download_file_size, "@@@@下载下来的ota包不完整，请检查！！！"

        self.android_mdm_page.confirm_received_alert(upgrade_tips)

        # check upgrade
        now_time = self.page.get_current_time()
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    break
                else:
                    self.page.refresh_page()
            else:
                self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                assert False, "@@@@30分钟还没有升级相应的安卓版本， 请检查！！！"
            self.page.time_sleep(3)

        self.android_mdm_page.device_boot(self.wifi_ip)
        after_upgrade_version = self.android_mdm_page.check_firmware_version()
        assert self.page.transfer_version_into_int(
            device_current_firmware_version) != self.page.transfer_version_into_int(after_upgrade_version), \
            "@@@@ota升级失败， 还是原来的版本%s！！" % device_current_firmware_version
        assert self.page.transfer_version_into_int(release_info["version"]) == \
               self.page.transfer_version_into_int(
                   after_upgrade_version), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version

    @allure.feature('MDM_test01')
    @allure.title("OTA- release again")
    def test_release_ota_again(self, go_to_ota_package_release, del_all_ota_release_log_after):
        exp_success_text = "Sync Ota Release Success"
        # exp_existed_text = "ota release already existed"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit", "version": "1.1.18"}
        # self.Page.click_package_release_page()
        if self.page.get_current_ota_release_log_total() == 0:
            assert False, "@@@@没有相应的释放记录，请检查！！！"
        self.page.select_release_log()
        self.page.release_again()
        self.page.time_sleep(3)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        # check the app action in ota upgrade logs, if download complete or upgrade complete, break
        alert.getAlert("请确认下载并且升级")
        self.page.go_to_new_address("ota/log")
        now_time = self.page.get_current_time()
        self.page.time_sleep(1)
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    break
                else:
                    self.page.refresh_page()
            else:
                self.page.refresh_page()
                # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1200):
                assert False, "@@@@20分钟还没有下载完相应的ota package， 请检查！！！"
            self.page.time_sleep(2)

        # check upgrade
        now_time = self.page.get_current_time()
        self.page.time_sleep(1)
        while True:
            info = self.page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    break
                else:
                    self.page.refresh_page()
            else:
                self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
            self.page.time_sleep(2)

    @allure.feature('MDM_test01')
    @allure.title("OTA- delete single log")
    def test_delete_single_ota_release_log(self, go_to_ota_upgrade_logs_page):
        exp_del_text = "Delete ota release <[NO Limit]> :Success"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        if self.page.get_release_log_length() != 0:
            org_log_length = self.page.get_release_log_length()
            print(org_log_length)
            self.page.search_single_release_log(release_info)
            self.page.delete_all_release_log(org_len=org_log_length, del_all=False)
