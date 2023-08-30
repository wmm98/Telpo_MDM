import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case_pack_pack_pack = case_pack.Optimize_Case()
alert = case_pack.AlertData()

log = case_pack.MyLog()


class TestAppPage:

    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.APPSPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("Apps-add app apk package")
    def test_add_new_apps(self, go_to_app_page):
        exp_success_text = "Success"
        package_info = {"package_name": "ComAssistant.apk", "file_category": "test",
                        "developer": "engineer", "description": "test"}

        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        info = {"file_name": file_path, "file_category": "test",
                "developer": "engineer", "description": "test"}
        self.page.page_load_complete()
        self.page.search_app_by_name(package_info["package_name"])
        search_list = self.page.get_apps_text_list()
        if len(search_list) == 0:
            self.page.click_add_btn()
            self.page.input_app_info(info)
            self.page.refresh_page()
            # check if add successfully
            self.page.search_app_by_name(package_info["package_name"])
            add_later_text_list = self.page.get_apps_text_list()
            if len(add_later_text_list) == 1:
                if package_info["package_name"] in add_later_text_list[0]:
                    assert True
                else:
                    assert False, "@@@添加apk失败， 请检查"
            else:
                assert False, "@@@添加apk失败， 请检查"

    @allure.feature('MDM_test02')
    @allure.title("Apps-delete apk package")
    def test_delete_single_app(self, go_to_app_page):
        package_info = {"package_name": "ComAssistant.apk", "file_category": "test",
                        "developer": "engineer", "description": "test"}
        self.page.page_load_complete()
        org_length = len(self.page.get_apps_text_list())
        self.page.search_app_by_name(package_info["package_name"])
        if len(self.page.get_apps_text_list()) == 1:
            self.page.click_delete_app_btn()
            self.page.refresh_page()
            new_length = len(self.page.get_apps_text_list())
            if org_length != (new_length + 1):
                assert False, "@@@@删除apk包失败请检查！！！"

    @allure.feature('MDM_test022')
    @allure.title("Apps-delete all app release log")
    def test_delete_all_app_release_app(self, go_to_app_release_log):
        self.page.page_load_complete()
        self.page.delete_all_app_release_log()

        assert self.page.get_current_app_release_log_total() == 0, "@@@@没有删除完了所有的app release log, 请检查!!!"

    @allure.feature('MDM_test022')
    @allure.title("Apps-release app")
    def test_release_app(self, go_to_app_page):
        release_info = {"package_name": "APKEditor_1_7_2.apk", "sn": "A250900P03100019",
                        "silent": "Yes", "version": "1.7.2", "package": "com.gmail.heagoo.apkeditor.pro"}
        self.page.page_load_complete()
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        # go to app release log
        self.page.go_to_new_address("apps/releases")
        self.page.page_load_complete()
        # self.page.check_release_log_info(send_time, release_info["sn"])

        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app release log， 请检查！！！"
            self.page.time_sleep(1)

    @allure.feature('MDM_test01')
    @allure.title("Apps- uninstall app")
    def test_uninstall_app(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page):
        app_release_address = "http://test.telpoai.com/apps/releases"
        app_upgrade_address = "http://test.telpoai.com/apps/logs"
        release_info = {"package_name": "APKEditor_1_9_10.apk", "sn": "A250900P03100019",
                        "silent": "Yes", "version": "1.9.10", "package": "com.gmail.heagoo.apkeditor.pro"}
        self.page.search_app_by_name(release_info["package_name"])

        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.page.click_uninstall_app_btn()
        self.page.input_uninstall_app_info(release_info)

        # go to app uninstall log
        # self.Page.go_to_new_address("apps/releases")
        # self.Page.check_release_log_info(release_info)

    @allure.feature('MDM_test01')
    @allure.title("Apps- release app again")
    def test_send_release_app_again(self, go_to_app_release_log):
        exp_release_success_text = "Sync App Release Success"
        release_info = {"package_name": "APKEditor_1_9_10.apk", "sn": "A250900P03100019",
                        "silent": "Yes", "version": "1.9.10", "package": "com.gmail.heagoo.apkeditor.pro"}
        self.page.search_app_release_log(release_info)
        if self.page.get_current_app_release_log_total() == 0:
            assert False, "@@@@没有相应的release app log, 请检查！！！"
        self.page.select_single_app_release_log()
        text = self.page.click_send_release_again()
        print(text)


















