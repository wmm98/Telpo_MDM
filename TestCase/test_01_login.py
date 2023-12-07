import TestCase
import allure
import pytest

log = TestCase.MyLog()
test_yaml = TestCase.yaml_data


class TestLogin:

    def setup_class(self):
        self.driver = TestCase.test_driver
        self.mdm_page = TestCase.MDMPage(self.driver, 40)
        self.android_mdm_page = TestCase.AndroidAimdmPage(TestCase.device_data, 5)
        self.android_mdm_page.open_usb_debug_btn()
        self.android_mdm_page.screen_keep_on()
        self.wifi_ip = TestCase.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.back_to_home()
        self.wait_times = 10

    def teardown_class(self):
        pass

    @allure.feature('MDM_test02_login')
    @allure.title("连接上wifi--辅助测试用例")  # 设置case的名字
    def test_connect_wifi_ok(self):
        print("&&&&&&&&&&&&&&")
        print(self.android_mdm_page.get_screen_size())

        wifi_available = test_yaml["android_device_info"]["available_wifi"]
        print(wifi_available)
        wifi_name_list = []
        wifi_psw_list = []
        for wifi in wifi_available:
            print(wifi_available[wifi])
            wifi_name_list.append(wifi_available[wifi]["name"])
            wifi_psw_list.append(wifi_available[wifi]["password"])
        print(wifi_name_list)
        print(wifi_psw_list)
        self.android_mdm_page.connect_available_wifi(wifi_name_list, wifi_psw_list)

    @allure.feature('MDM_test02_login1111')
    @allure.story("MDM_test02_login")
    @allure.title("login is ok--辅助测试用例")  # 设置case的名字
    @pytest.mark.dependency(name="test_login_ok", scope='package')
    def test_login_ok(self):
        username = test_yaml['website_info']['test_user']
        password = test_yaml['website_info']['test_password']

        self.mdm_page.login_ok(username, password)


if __name__ == '__main__':
    case = TestLogin()
    case.test_login_ok()
