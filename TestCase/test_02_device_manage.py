import allure
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common.element_operations import ElementsOperations
from utils.base_web_driver import BaseWeb
import pytest


class TestDeviceManage:

    def setup_class(self):
        # self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        # self.driver.maximize_window()
        # url = 'https://mdm.telpoai.com/login'
        # # 窗口最大化
        # self.driver.get(url)

        self.driver = BaseWeb().driver
        self.element_func = ElementsOperations(self.driver)
        self.wait_times = 10

    def teardown_class(self):
        pass

    @allure.feature('MDM_test01')
    @allure.title("设备页面")  # 设置case的名字
    @pytest.mark.dependency(depends=["TestCase/test_01_login.py::test_login_ok"])
    def test_go_to_devices_page(self):
        print("运行到这里")
        print(self.driver.title)