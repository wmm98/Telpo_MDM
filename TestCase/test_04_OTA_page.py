import allure
from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Devices_Page import DevicesPage
from Page.Message_Page import MessagePage
from Page.Telpo_MDM_Page import TelpoMDMPage
from Page.System_Page import SystemPage
from Page.OTA_Page import OTAPage
import time
from Common.excel_data import ExcelData
from Conf.Config import Config
from Common.simply_case import Optimize_Case
from Common.DealAlert import AlertData
from Page.Release_Device_Page import ReleaseDevicePage

conf = Config()
excel = ExcelData()
opt_case = Optimize_Case()
alert = AlertData()

log = Log.MyLog()


class TestOTAPage:

    def setup_class(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = OTAPage(self.driver, 40)
        self.system_page = SystemPage(self.driver, 40)

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("OTA-Upgrade Packages Page")
    def test_upgrade_package_page(self, go_to_ota_upgrade_package_page):
        # self.page.click_OTA_btn()
        # self.page.click_upgrade_packages()
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
    @allure.title("OTA-release OTA package")
    def test_release_OTA_package(self):
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}

        self.page.refresh_page()
        # search package
        self.page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.page.get_package_ele(release_info["package_name"])
        # if device is existed, click
        self.page.click_release_btn()
        self.page.input_release_OTA_package(release_info)

        text = self.page.click_alert_release_btn()
        # text = self.page.get_alert_text()
        if exp_success_text in text:
            self.page.click_package_release_page()
            # check release log
            self.page.check_single_release_info(release_info)
        elif exp_existed_text in text:
            self.page.refresh_page()

    @allure.feature('MDM_test01')
    @allure.title("OTA- release again")
    def test_release_ota_again(self, go_to_ota_upgrade_logs_page):
        # self.page.refresh_page()
        time.sleep(1)
        exp_success_text = "Sync Ota Release Success"
        # exp_existed_text = "ota release already existed"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        # self.page.click_package_release_page()
        self.page.check_single_release_info(release_info)
        self.page.search_single_release_log(release_info, count=True)
        self.page.select_release_log()
        self.page.release_again()
        while True:
            if exp_success_text in self.system_page.get_latest_action():
                alert.getAlert("请点击下载，升级")
                break
            else:
                self.page.release_again()
            time.sleep(1)
            if time.time() > self.page.return_end_time():
                assert False, "@@@再一次释OTA package放失败， 请检查！！！"

    @allure.feature('MDM_test01')
    @allure.title("OTA- delete all log")
    def test_delete_all_ota_release_logs(self, go_to_ota_upgrade_logs_page):
        time.sleep(1)
        exp_del_text = "Delete ota release <[NO Limit]> :Success"
        if self.page.get_release_log_length() != 0:
            self.page.delete_all_release_log()

    @allure.feature('MDM_test01')
    @allure.title("OTA- delete single log")
    def test_delete_single_ota_release_log(self, go_to_ota_upgrade_logs_page):
        time.sleep(1)
        exp_del_text = "Delete ota release <[NO Limit]> :Success"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        if self.page.get_release_log_length() != 0:
            org_log_length = self.page.get_release_log_length()
            print(org_log_length)
            self.page.search_single_release_log(release_info)
            self.page.delete_all_release_log(org_len=org_log_length, del_all=False)
