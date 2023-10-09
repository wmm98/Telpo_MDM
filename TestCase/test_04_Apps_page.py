import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
test_yml = case_pack.yaml_data
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()

log = case_pack.MyLog()

package_infos = [{"package_name": test_yml['app_info']['low_version_app'], "file_category": "test",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['high_version_app'], "file_category": "test",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app'], "file_category": "test01",
                  "developer": "engineer", "description": "test"}]


class TestAppPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.APPSPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.device_sn = self.android_mdm_page.get_device_sn()

    def teardown_class(self):
        self.android_mdm_page.del_all_downloaded_apk()
        self.page.refresh_page()

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps-添加APK包")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @pytest.mark.parametrize('package_info', package_infos)
    def test_add_new_apps(self, package_info, go_to_app_page):
        exp_success_text = "Success"
        # package_info = {"package_name": "Bus_Recharge_System_1.0.1_20220615.apk", "file_category": "test",
        #                 "developer": "engineer", "description": "test"}
        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        info = {"file_name": file_path, "file_category": "test",
                "developer": "engineer", "description": "test"}
        self.page.search_app_by_name(package_info["package_name"])
        search_list = self.page.get_apps_text_list()
        if len(search_list) == 0:
            if package_info["file_category"] not in self.page.get_app_categories_list():
                self.page.add_app_category(package_info["file_category"])
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

    @allure.feature('MDM_APP-test01')
    @allure.title("Apps-辅助测试用例")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_delete_all_app_release_app(self, go_to_app_release_log):
        self.page.page_load_complete()
        self.page.delete_all_app_release_log()
        assert self.page.get_current_app_release_log_total() == 0, "@@@@没有删除完了所有的app release log, 请检查!!!"

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps-推送低版本的APP")
    @pytest.mark.dependency(name="test_release_app_ok", scope='package')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_low_version_app(self, del_all_app_release_log, del_all_app_uninstall_release_log):
        release_info = {"package_name": test_yml['app_info']['low_version_app'], "sn": self.device_sn,
                        "silent": "Yes"}
        # apk_info = {"package_name": "ComAssistant.apk", "sn": "A250900P03100019",
        #                 "silent": "Yes", "version": "1.1"}

        # release_info = {"package_name": "ComAssistant.apk", "sn": "A250900P03100019",
        #                 "silent": "Yes"}
        file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])

        # check if the app is existed, if existed, uninstall, else push
        # if self.android_mdm_page.app_is_installed(release_info["package"]):
        #     self.android_mdm_page.uninstall_app(release_info["package"])

        # app_size_mdm = self.page.get_app_size()  for web
        # check app size(bytes) in windows
        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)

        # go to app page
        self.page.go_to_new_address("apps")
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        # go to app release log
        self.page.go_to_new_address("apps/releases")
        # self.page.check_release_log_info(send_time, release_info["sn"])

        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            try:
                release_log = self.page.get_app_latest_release_log_list(send_time, release_info)
            except Exception as e:
                print(e)
            release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app release log， 请检查！！！"
            self.page.time_sleep(3)

        # check if the upgrade log appeared, if appeared, break
        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            release_len = len(self.page.get_app_latest_upgrade_log(send_time, release_info))
            if release_len == 1:
                break
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
            self.page.time_sleep(5)

        """
        Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
         4: upgrading complete, 5: downloading failed, 6: upgrading failed)
         0: Uninstall completed
        """
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        now_time = self.page.get_current_time()
        while True:
            action = self.page.get_app_latest_upgrade_log(send_time, release_info)[0]["Action"]
            if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                    or self.page.get_action_status(action) == 3:
                # check the app size in device, check if app download fully
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                    assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"

                size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
                print("终端下载后的的size大小：", size)
                if app_size != size:
                    assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                break
            else:
                self.page.refresh_page()
            # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1200):
                assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
            self.page.time_sleep(5)

        # check upgrade
        now_time = self.page.get_current_time()
        while True:
            action = self.page.get_app_latest_upgrade_log(send_time, release_info)[0]["Action"]
            print("action", action)
            if self.page.get_action_status(action) == 4:
                if self.android_mdm_page.app_is_installed(release_info["package"]):
                    break
                else:
                    assert False, "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
            else:
                self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps-推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装")
    @pytest.mark.dependency(depends=["test_release_app_ok"], scope='package')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_high_version_app_cover_low_version_app(self, del_all_app_release_log, del_all_app_uninstall_release_log):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes"}

        file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # app_size_mdm = self.page.get_app_size()  for web
        # check app size(bytes) in windows
        app_size = self.page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)

        # go to app page
        self.page.go_to_new_address("apps")
        self.page.search_app_by_name(release_info["package_name"])
        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(3)
        self.page.click_release_app_btn()
        self.page.input_release_app_info(release_info)
        # go to app release log
        self.page.go_to_new_address("apps/releases")
        # self.page.check_release_log_info(send_time, release_info["sn"])

        now_time = self.page.get_current_time()
        # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info))
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

        # check if the upgrade log appeared, if appeared, break
        self.page.go_to_new_address("apps/logs")
        now_time = self.page.get_current_time()
        while True:
            release_len = len(self.page.get_app_latest_upgrade_log(send_time, release_info))
            if release_len == 1:
                break
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
            self.page.time_sleep(3)

        """
        Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
         4: upgrading complete, 5: downloading failed, 6: upgrading failed)
         0: Uninstall completed
        """
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                if self.page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                        or self.page.get_action_status(action) == 3:
                    # check the app size in device, check if app download fully
                    shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                    if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"

                    size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
                    print("终端下载后的的size大小：", size)
                    if app_size != size:
                        assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                    break
                else:
                    self.page.refresh_page()
                # wait 20 mins
            if self.page.get_current_time() > self.page.return_end_time(now_time, 1200):
                assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
            self.page.time_sleep(5)

        # check upgrade
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        if version_installed == self.page.transfer_version_into_int(release_info["version"]):
                            break
                        else:
                            assert False, "@@@@平台显示已经完成覆盖安装了app, 终端发现没有安装高版本的app，还是原来的版本， 请检查！！！！"
                else:
                    self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有静默安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)
        log.info("*******************静默安装完成***************************")

        # uninstall app and check if app would be installed again in 10min
        self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
        # check upgrade
        send_time_again = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                  case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(4)
        now_time = self.page.get_current_time()
        while True:
            upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.page.get_action_status(action) == 4:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        if version_installed == self.page.transfer_version_into_int(release_info["version"]):
                            break
                        else:
                            assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
                else:
                    self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 610):
                log.error("@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！")
                assert False, "@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)
        log.info("*******************卸载后重新安装成功***************************")
        # uninstall app and reboot, check if app would be reinstalled again
        self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        self.android_mdm_page.device_existed(self.wifi_ip)
        self.android_mdm_page.device_boot_complete()
        # check upgrade
        send_time_again = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                  case_pack.time.localtime(self.page.get_current_time()))
        self.page.time_sleep(4)
        now_time = self.page.get_current_time()
        while True:
            action = self.page.get_app_latest_upgrade_log(send_time_again, release_info)[0]["Action"]
            print("action", action)
            if self.page.get_action_status(action) == 4:
                if self.android_mdm_page.app_is_installed(release_info["package"]):
                    version_installed_again = self.page.transfer_version_into_int(
                        self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                    if version_installed_again == self.page.transfer_version_into_int(release_info["version"]):
                        break
                    else:
                        assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
            else:
                self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 610):
                log.error("@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！")
                assert False, "@@@@卸载后超过10分钟还没有安装完相应的app， 请检查！！！"
            self.page.time_sleep(5)

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps- 在原有的记录上再次释放app")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_send_release_install_app_again(self, go_to_app_release_log, del_all_app_release_log_after):
        exp_release_success_text = "Sync App Release Success"
        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                        "silent": "Yes"}
        # self.page.search_app_release_log(release_info)
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # go to app release page
        self.page.go_to_new_address("apps/releases")
        if self.page.get_current_app_release_log_total() == 0:
            assert False, "@@@@没有相应的release app log, 请检查！！！"
        self.page.select_single_app_release_log()
        self.page.click_send_release_again()

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps- 卸载正在运行的APP")
    # @pytest.mark.dependency(depends=["test_release_app_ok"], scope='package')
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_uninstall_app(self, del_all_app_release_log, del_all_app_uninstall_release_log):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes"}
        file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        package = self.page.get_apk_package_name(file_path)
        release_info["package"] = package

        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # go to app release page
        self.page.go_to_new_address("apps")
        self.page.search_app_by_name(release_info["package_name"])

        app_list = self.page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]

        # start app and then uninstall it， added recently
        self.android_mdm_page.start_app(release_info["package"])
        # self.android_mdm_page
        self.page.click_uninstall_app_btn()
        self.page.input_uninstall_app_info(release_info)
        self.page.time_sleep(3)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.page.get_current_time()))
        # go to app uninstall log
        self.page.go_to_new_address("apps/appUninstall")
        now_time = self.page.get_current_time()
        while True:
            release_len = len(self.page.get_app_latest_release_log_list(send_time, release_info, uninstall=True))
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次uninstall app，有多条释放记录，请检查！！！"
            else:
                self.page.refresh_page()
            if self.page.get_current_time() > self.page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app uninstall release log， 请检查！！！"

        self.page.go_to_new_address("apps/uninstalllogs")
        now_time = self.page.get_current_time()
        while True:
            action = self.page.get_app_latest_uninstall_log(send_time, release_info)[0]["Action"]
            print("action", action)
            if self.page.get_action_status(action) == 0:
                break
            else:
                self.page.refresh_page()
            # wait upgrade 3 mins at most
            if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有卸载完相应的app， 请检查！！！"
            self.page.time_sleep(3)

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps- release app again")
    def test_send_release_uninstall_app_again(self, del_all_app_release_log, del_all_app_uninstall_release_log_after):
        exp_release_success_text = "Sync App Release Success"
        # release_info = {"package_name": "APKEditor_1_9_10.apk", "sn": "A250900P03100019",
        #                 "silent": "Yes", "version": "1.9.10", "package": "com.gmail.heagoo.apkeditor.pro"}
        release_info = {"package_name": "ComAssistant.apk", "sn": self.device_sn,
                        "silent": "Yes", "version": "1.1", "package": "com.bjw.ComAssistant"}
        # check if device is online
        self.page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # go to app release page
        self.page.go_to_new_address("apps/appUninstall")
        if self.page.get_current_app_release_log_total() == 0:
            assert False, "@@@@没有相应的release app log, 请检查！！！"
        self.page.select_single_app_release_log()
        self.page.click_send_release_again()

    @allure.feature('MDM_APP-test022')
    @allure.title("Apps-删除APK包")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_delete_single_app(self, go_to_app_page):
        package_info = {"package_name": test_yml['app_info']['other_app'], "file_category": "test",
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
