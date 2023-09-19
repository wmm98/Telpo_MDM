import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()


class TestNetworkCases:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.DevicesPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.serial = case_pack.device_data["usb_device_info"]["device"]
        self.ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.device_unlock_USB()

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test_usb_debug')
    def test_usb_debug(self):
        print("================这是USB调试模式下==================================")
        print(self.android_mdm_page.get_app_installed_list_USB())
        print("================这是WIFI调试模式下==================================")
        print(self.android_mdm_page.get_app_installed_list())
        self.android_mdm_page.disconnect_ip(self.ip)
        self.android_mdm_page.close_wifi_btn()
        self.page.time_sleep(3)
        self.android_mdm_page.open_wifi_btn()
        self.page.time_sleep(2)
        while True:
            res = self.android_mdm_page.wifi_open_status()
            print(res)
            if res:
                break
            self.page.time_sleep(2)

        self.android_mdm_page.ping_network(times=4)
        # self.android_mdm_page.send_adb_command_USB("reboot")
        self.android_mdm_page.confirm_wifi_adb_connected(self.ip)
        self.android_mdm_page.device_boot_complete()
        print(self.android_mdm_page.get_app_installed_list())












