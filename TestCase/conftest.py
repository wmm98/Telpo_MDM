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
# from utils.base_web_driver import BaseWebDriver
# from Page import Telpo_MDM_Page, Devices_Page, OTA_Page, Apps_Page
import TestCase

driver = TestCase.test_driver
device_page = TestCase.DevicesPage(driver, 40)
ota_page = TestCase.OTAPage(driver, 40)
app_page = TestCase.APPSPage(driver, 40)
content_page = TestCase.ContentPage(driver, 40)
android_page = TestCase.AndroidAimdmPage(TestCase.device_data, 30)
wifi_ip = TestCase.device_data["wifi_device_info"]["ip"]


@pytest.fixture()
def uninstall_system_app():
    android_page.rm_file("system/app/%s" % TestCase.yaml_data['app_info']['low_version_app'])
    android_page.reboot_device(wifi_ip)
    android_page.reboot_device(wifi_ip)
    android_page.uninstall_multi_apps(TestCase.yaml_data['app_info'])
    yield
    android_page.rm_file("system/app/%s" % TestCase.yaml_data['app_info']['low_version_app'])
    android_page.reboot_device(wifi_ip)
    android_page.reboot_device(wifi_ip)
    android_page.uninstall_multi_apps(TestCase.yaml_data['app_info'])


@pytest.fixture()
def uninstall_multi_apps():
    android_page.uninstall_multi_apps(TestCase.yaml_data["app_info"])
    yield
    android_page.uninstall_multi_apps(TestCase.yaml_data["app_info"])


@pytest.fixture()
def del_download_apk():
    android_page.del_all_downloaded_apk()
    yield
    android_page.del_all_downloaded_apk()


@pytest.fixture()
def unlock_screen():
    android_page.device_unlock()
    yield


@pytest.fixture()
def delete_ota_package_relate():
    android_page.del_all_downloaded_zip()
    android_page.del_updated_zip()
    yield
    android_page.del_all_downloaded_zip()
    android_page.del_updated_zip()


@pytest.fixture()
def connected_wifi_adb():
    yield
    android_page.confirm_wifi_adb_connected(TestCase.wifi_ip)
    android_page.device_existed(TestCase.wifi_ip)
    android_page.device_boot_complete()


@pytest.fixture()
def return_device_page():
    yield
    device_page.go_to_new_address("devices")
    # device_page.click_devices_btn()
    # # click devices list btn  -- just for test version
    # device_page.click_devices_list_btn()


@pytest.fixture()
def go_to_and_return_device_page():
    device_page.go_to_new_address("devices")
    yield
    device_page.go_to_new_address("devices")


@pytest.fixture()
def go_to_device_page():
    device_page.go_to_new_address("devices")
    yield


@pytest.fixture()
def go_to_ota_upgrade_logs_page():
    ota_page.go_to_new_address("ota/log")
    yield


@pytest.fixture()
def go_to_ota_upgrade_package_page():
    ota_page.go_to_new_address("ota")
    yield


@pytest.fixture()
def go_to_ota_package_release():
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
def del_all_ota_release_log_before():
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()
    yield


@pytest.fixture()
def del_all_ota_release_log_after():
    yield
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()


@pytest.fixture()
def del_all_ota_release_log():
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()
    yield
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()


@pytest.fixture()
def go_to_ota_page():
    ota_page.go_to_new_address("ota")
    yield


@pytest.fixture()
def del_all_app_release_log_after():
    yield
    app_page.go_to_new_address("apps/releases")
    app_page.delete_all_app_release_log()


@pytest.fixture()
def go_to_content_page():
    content_page.go_to_new_address("content")
    yield


@pytest.fixture()
def del_all_content_release_logs():
    content_page.go_to_new_address("content/release")
    content_page.delete_all_content_release_log()
    yield
    content_page.go_to_new_address("content/release")
    content_page.delete_all_content_release_log()


@pytest.fixture()
def go_to_content_release_page():
    content_page.go_to_new_address("content/release")
    yield


@pytest.fixture()
def go_to_content_upgrade_page():
    content_page.go_to_new_address("content/log")
    yield


@pytest.fixture()
def del_all_app_uninstall_release_log():
    app_page.go_to_new_address("apps/appUninstall")
    app_page.delete_all_app_release_log()
    yield


@pytest.fixture()
def del_all_app_uninstall_release_log_after():
    yield
    app_page.go_to_new_address("apps/appUninstall")
    app_page.delete_all_app_release_log()


@pytest.fixture()
def go_to_app_release_log():
    app_page.go_to_new_address("apps/releases")
    yield


@pytest.fixture()
def go_to_app_uninstall_release_log():
    app_page.go_to_new_address("apps/appUninstall")
    yield


@pytest.fixture()
def connect_wifi_adb():
    yield
    android_page.open_wifi_btn()
    android_page.confirm_wifi_adb_connected(TestCase.wifi_ip)
