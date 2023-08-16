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
    def test_add_apps(self, go_to_app_page):
        exp_success_text = "Success"
        package_info = {"package_name": "ComAssistant.apk", "file_category": "test",
                        "developer": "test engineer", "description": "just for test"}

        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        info = {"file_name": file_path, "file_category": "test",
                "developer": "engineer", "description": "test"}
        self.page.search_app_by_name(package_info["package_name"])
        search_list = self.page.get_apps_text_list()
        if len(search_list) == 0:
            self.page.click_add_btn()
            self.page.input_app_info(info)
            # self.page.click_save_add_app()
            text = self.page.get_alert_text()
            print(text)
            self.page.check_add_app_save_btn()
            if exp_success_text in text:
                self.page.search_app_by_name(package_info["package_name"])
                add_later_text_list = self.page.get_apps_text_list()
                if len(add_later_text_list) == 1:
                    if package_info["package_name"] in add_later_text_list[0]:
                        assert True
                    else:
                        assert False, "@@@添加apk失败， 请检查"
                else:
                    assert False, "@@@添加apk失败， 请检查"
            else:
                self.page.refresh_page()
                self.page.search_app_by_name(package_info["package_name"])
                add_later_text_list = self.page.get_apps_text_list()
                if len(add_later_text_list) == 1:
                    if package_info["package_name"] in add_later_text_list[0]:
                        assert True
                    else:
                        assert False, "@@@添加apk失败， 请检查"
                else:
                    assert False, "@@@添加apk失败， 请检查"





