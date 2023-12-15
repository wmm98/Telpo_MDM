import TestCase
import allure
import pytest

log = TestCase.MyLog()
test_yaml = TestCase.yaml_data
conf = TestCase.Config()


class TestLogin:

    def setup_class(self):
        self.api_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yaml["work_app"]["api_txt"]
        self.driver = TestCase.test_driver
        self.mdm_page = TestCase.MDMPage(self.driver, 40)
        self.app_page = TestCase.APPSPage(self.driver, 40)
        self.ota_page = TestCase.OTAPage(self.driver, 40)
        self.device_page = TestCase.DevicesPage(self.driver, 40)
        self.android_mdm_page = TestCase.AndroidAimdmPage(TestCase.device_data, 5)
        self.android_mdm_page.open_usb_debug_btn()
        # self.android_mdm_page.confirm_app_installed(
        #     conf.project_path + "\\Param\\Work_APP\\%s" % test_yaml["work_app"]["aidmd_apk"])
        # self.android_mdm_page.push_file_to_device(self.api_path,
        #                                           self.android_mdm_page.get_internal_storage_directory() + "/")
        self.android_mdm_page.screen_keep_on()
        self.wifi_ip = TestCase.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.back_to_home()
        self.wait_times = 10
        self.wifi_flag = 0

    def teardown_class(self):
        pass

    @allure.feature('MDM_test02_login')
    @allure.title("连接上wifi/登录--辅助测试用例")  # 设置case的名字
    @pytest.mark.dependency(name="test_login_ok", scope='package')
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_connect_wifi_and_login_ok(self):
        self.android_mdm_page.screen_keep_on()
        if self.android_mdm_page.get_current_wlan() is None:
            # self.android_mdm_page.clear_recent_app_USB()
            self.android_mdm_page.open_wifi_btn()
            # self.android_mdm_page.time_sleep(5)
            self.android_mdm_page.confirm_open_wifi_page()
            self.android_mdm_page.confirm_wifi_switch_open()
            self.android_mdm_page.time_sleep(10)
            if self.android_mdm_page.get_current_wlan() is None:
                wifi_available = test_yaml["android_device_info"]["available_wifi"]
                wifi_list = []
                for wifi in wifi_available:
                    wifi_list.append(wifi_available[wifi])

                self.android_mdm_page.connect_available_wifi(wifi_list)
                # self.android_mdm_page.clear_recent_app_USB()
        self.android_mdm_page.ping_network(timeout=180)

        username = test_yaml['website_info']['test_user']
        password = test_yaml['website_info']['test_password']
        #
        self.mdm_page.login_ok(username, password)

        self.device_page.go_to_new_address("devices")
        devices_sn = [device["SN"] for device in self.device_page.get_dev_info_list()]
        device_sn = self.android_mdm_page.get_device_sn()
        devices_list = {"SN": device_sn, "name": "aut" + device_sn}
        if device_sn not in devices_sn:
            # check if device model is existed, if not, add model
            if "automation_debug" not in self.device_page.get_models_list():
                self.device_page.click_model()
                self.device_page.add_model("automation_debug")
                self.device_page.refresh_page()
            # check if device category is existed, if not, add category
            if not self.device_page.category_is_existed("test_debug"):
                self.device_page.click_category()
                self.device_page.add_category("test_debug")
            self.device_page.click_new_btn()
            self.device_page.add_devices_info(devices_list, cate_model=False)
            self.device_page.refresh_page()
        self.android_mdm_page.confirm_app_installed(
            conf.project_path + "\\Param\\Work_APP\\%s" % test_yaml["work_app"]["aidmd_apk"])
        self.android_mdm_page.push_file_to_device(self.api_path,
                                                  self.android_mdm_page.get_internal_storage_directory() + "/")
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.device_page.refresh_page()

    @allure.feature('MDM_test02_login')
    @allure.title("OTA-添加ota升级包-- 辅助测试用例")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_add_OTA_package_and_cate(self, go_to_ota_page):
        exp_existed_text = "ota already existed"
        exp_success_text = "success"
        package_info = {"package_name": test_yaml['ota_packages_info']['package_name'], "file_category": "test",
                        "plat_form": test_yaml['ota_packages_info']['platform']}
        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        ota_info = {"file_name": file_path, "file_category": package_info["file_category"],
                    "plat_form": package_info["plat_form"]}
        # check if category is existed
        try:
            if len(self.ota_page.get_ota_categories_list()) == 0:
                self.ota_page.add_ota_category("test")
                self.ota_page.refresh_page()
        except Exception as e:
            print(e)
        # check if ota package is existed, if not, add package, else skip
        self.ota_page.search_device_by_pack_name(package_info["package_name"])
        if len(self.ota_page.get_ota_package_list()) == 0:
            self.ota_page.click_add_btn()
            self.ota_page.input_ota_package_info(ota_info)
            self.ota_page.click_save_add_ota_pack()
            self.ota_page.search_device_by_pack_name(package_info["package_name"])
            assert len(self.ota_page.get_ota_package_list()) == 1, "@@@添加失败！！！"

    @allure.feature('MDM_test02_login')
    @allure.title("Apps-添加APK包--辅助测试用例")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    # @pytest.mark.parametrize('package_info', package_infos)
    def test_add_cate_and_apps(self, go_to_app_page):
        exp_success_text = "Success"
        # package_info = {"package_name": "Bus_Recharge_System_1.0.1_20220615.apk", "file_category": "test",
        #                 "developer": "engineer", "description": "test"}
        apks = test_yaml["app_info"]
        # apks.update(test_yml["system_app"])
        print(apks)
        for apk in list(apks.values()):
            file_path = conf.project_path + "\\Param\\Package\\%s" % apk
            if self.app_page.get_app_categories_list() == 0:
                self.app_page.add_app_category("test")
            if len(self.app_page.get_apps_text_list()) == 0:
                self.app_page.click_add_btn()
                self.app_page.input_app_info(file_path)
                self.app_page.refresh_page()
            else:
                self.app_page.search_app_by_name(apk)
                search_list = self.app_page.get_apps_text_list()
                if len(search_list) == 0:
                    self.app_page.click_add_btn()
                    self.app_page.input_app_info(file_path)
                    self.app_page.refresh_page()

    @allure.feature('MDM_test02_login11111')
    @allure.story("MDM_test02_login")
    @allure.title("login is ok--辅助测试用例")  # 设置case的名字
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    def test_login_ok(self):
        username = test_yaml['website_info']['test_user']
        password = test_yaml['website_info']['test_password']

        self.mdm_page.login_ok(username, password)


if __name__ == '__main__':
    case = TestLogin()
    case.test_login_ok()
