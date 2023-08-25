"""

# @allure.feature # 用于定义被测试的功能，被测产品的需求点
# @allure.story # 用于定义被测功能的用户场景，即子功能点
# @allure.severity #用于定义用例优先级
# @allure.issue #用于定义问题表识，关联标识已有的问题，可为一个url链接地址
# @allure.testcase #用于用例标识，关联标识用例，可为一个url链接地址

# @allure.attach # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
# @pytest.allure.step # 用于将一些通用的函数作为测试步骤输出到报告，调用此函数的地方会向报告中输出步骤
# allure.environment(environment=env) #用于定义environment

"""
import pytest
from utils.base_web_driver import BaseWebDriver
from Page import Telpo_MDM_Page, Devices_Page, OTA_Page, Apps_Page

base_driver = BaseWebDriver()
driver = base_driver.get_web_driver()
device_page = Devices_Page.DevicesPage(driver, 40)
ota_page = OTA_Page.OTAPage(driver, 40)
app_page = Apps_Page.APPSPage(driver, 40)


@pytest.fixture()
def return_device_page():
    yield
    device_page.go_to_new_address("devices")
    # device_page.click_devices_btn()
    # # click devices list btn  -- just for test version
    # device_page.click_devices_list_btn()


@pytest.fixture()
def go_to_ota_upgrade_logs_page():
    ota_page.click_OTA_btn()
    ota_page.click_package_release_page()
    yield


@pytest.fixture()
def go_to_ota_upgrade_package_page():
    ota_page.go_to_new_address("ota")
    yield


@pytest.fixture()
def go_to_ota_package_releases():
    app_page.go_to_new_address("ota/release")
    yield


@pytest.fixture()
def go_to_app_page():
    app_page.go_to_new_address("apps")
    yield


@pytest.fixture()
def del_all_app_release_log():
    app_page.go_to_new_address("apps/releases")
    app_page.delete_all_app_release_log()
    yield


@pytest.fixture()
def del_all_app_uninstall_release_log():
    app_page.go_to_new_address("apps/appUninstall")
    app_page.delete_all_app_release_log()
    yield


@pytest.fixture()
def go_to_app_release_log():
    app_page.go_to_new_address("apps/releases")
    yield
