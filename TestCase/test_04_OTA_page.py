import allure
from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Devices_Page import DevicesPage
from Page.Message_Page import MessagePage
from Page.Telpo_MDM_Page import TelpoMDMPage
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

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("OTA-Upgrade Packages Page")
    def test_upgrade_package_page(self):
        self.page.click_OTA_btn()
        self.page.click_upgrade_packages()

    @allure.feature('MDM_test02')
    @allure.title("OTA-release OTA package")
    def test_release_OTA_package(self):
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": "TPS900 package - V 1.1.18", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit", }
        self.page.click_upgrade_packages()
        ele = self.page.get_package_ele(release_info["package_name"])
        self.page.click_release_btn(ele)
        self.page.input_release_OTA_package(release_info)
        self.page.click_alert_release_btn()
        text = self.page.get_alert_text()
        if self.page.alert_is_existed():
            self.page.click_alert_release_btn()
        if exp_success_text in text:
            pass












