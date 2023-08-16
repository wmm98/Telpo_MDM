import allure
from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Devices_Page import DevicesPage
from Page.Apps_Page import APPSPage
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


class TestAppPage:

    def setup_class(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = APPSPage(self.driver, 40)
        self.system_page = SystemPage(self.driver, 40)

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("Apps-add app apk package")
    def test_go_to_apps_page(self, go_to_app_page):
        package_info = {"package_name": "ComAssistant.apk", "file_category": "test",
                        "developer": "test engineer", "description": "just for test"}

        self.page.click_private_app_btn()

