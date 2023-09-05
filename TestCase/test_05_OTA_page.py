import allure
import TestCase as case_pack
import pytest


conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()


class TestOTAPage:

    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.OTAPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("OTA-Upgrade Packages Page")
    def test_upgrade_package_page(self, go_to_ota_upgrade_package_page):
        # self.Page.click_OTA_btn()
        # self.Page.click_upgrade_packages()
        self.page.page_load_complete()

    @allure.feature('MDM_test02')
    @allure.title("OTA-Delete OTA package")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_delete_OTA_package(self):
        package_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "file_category": "test",
                        "plat_form": "Android"}
        self.page.refresh_page()
        self.page.search_device_by_pack_name(package_info["package_name"])
        if len(self.page.get_ota_package_list()) == 1:
            self.page.delete_ota_package()
            self.page.refresh_page()
            self.page.search_device_by_pack_name(package_info["package_name"])
            assert len(self.page.get_ota_package_list()) == 0, "@@@@删除失败，请检查！！！"

    @allure.feature('MDM_test02')
    @allure.title("OTA-Add OTA package")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_add_OTA_package(self):
        exp_existed_text = "ota already existed"
        exp_success_text = "success"
        package_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "file_category": "test",
                        "plat_form": "Android"}
        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        ota_info = {"file_name": file_path, "file_category": package_info["file_category"],
                    "plat_form": package_info["plat_form"]}
        # check if ota package is existed, if not, add package, else skip
        self.page.refresh_page()
        self.page.search_device_by_pack_name(package_info["package_name"])
        if len(self.page.get_ota_package_list()) == 0:
            self.page.click_add_btn()
            self.page.input_ota_package_info(ota_info)
            self.page.click_save_add_ota_pack()
            self.page.search_device_by_pack_name(package_info["package_name"])
            assert len(self.page.get_ota_package_list()) == 1, "@@@添加失败！！！"

    @allure.feature('MDM_test01')
    @allure.title("OTA- delete all ota release log")
    def test_release_delete_all_ota_release_log(self, go_to_ota_package_release):
        self.page.delete_all_ota_release_log()
        self.page.time_sleep(3)
        assert self.page.get_current_ota_release_log_total() == 0, "@@@@没有删除完了所有的app release log, 请检查!!!"

    @allure.feature('MDM_test02')
    @allure.title("OTA-release OTA package")
    def test_release_OTA_package(self, del_all_ota_release_log, go_to_ota_page):
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit", "version": "1.1.18"}
        # search package
        self.page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        # if device is existed, click
        self.page.click_release_btn()
        self.page.input_release_OTA_package(release_info)
        self.page.time_sleep(3)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
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

        alert.getAlert("请确认下载并且升级")
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
                # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1200):
                assert False, "@@@@20分钟还没有下载完相应的ota package， 请检查！！！"
            self.page.time_sleep(2)

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
            if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
            self.page.time_sleep(2)

    @allure.feature('MDM_test02')
    @allure.title("OTA- release again")
    def test_release_ota_again(self, go_to_ota_package_release, del_all_ota_release_log_after):
        exp_success_text = "Sync Ota Release Success"
        # exp_existed_text = "ota release already existed"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
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
