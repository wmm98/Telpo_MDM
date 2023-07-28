import allure
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common.element_operations import ElementsOperations
from utils.base_web_driver import BaseWeb
import pytest
from Common import Log

log = Log.MyLog()


class TestDeviceManage:

    def setup_class(self):
        self.driver = BaseWeb().get_web_driver()
        self.element_func = ElementsOperations(self.driver)

    def teardown_class(self):
        pass

    @allure.feature('MDM_test01')
    @allure.title("设备页面")  # 设置case的名字
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    def test_go_to_devices_page(self):
        print(self.driver.title)
        log.info("当前页面标题为 %s" % self.driver.title)
        loc_devices_page_btn = (By.XPATH, "/html/body/div[1]/aside[1]/div/div[4]/div/div/nav/ul/li[2]/a/p")
        device_page_url = "https://mdm.telpoai.com/devices"
        loc_main_title = (By.CLASS_NAME, "m-0")
        exp_main_title = "Total Devices"

        try:
            # 点击
            self.element_func.web_driver_wait_until(EC.presence_of_element_located(loc_devices_page_btn))
            self.element_func.element_click(loc_devices_page_btn)

            # 验证当前页面
            self.element_func.web_driver_wait_until(EC.url_to_be(device_page_url))
            log.info("当前页面url: %s" % device_page_url)
            self.element_func.web_driver_wait_until(EC.presence_of_element_located(loc_main_title))
            main_title = self.element_func.element_find(loc_main_title)
            print(main_title.text)

            assert exp_main_title in main_title.text
        except Exception as e:
            log.error(str(e))
            assert False


    # def


