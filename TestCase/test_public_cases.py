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
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app_limit_network_A'], "file_category": "test01",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app_limit_network_B'], "file_category": "test01",
                  "developer": "engineer", "description": "test"}
                 ]


class TestPubilcPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.device_page = case_pack.DevicesPage(self.driver, 40)
        self.app_page = case_pack.APPSPage(self.driver, 40)
        self.ota_page = case_pack.OTAPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.content_page = case_pack.ContentPage(self.driver, 40)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.del_all_content_file()
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.reboot_device(self.wifi_ip)

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_all_content_file()
        self.app_page.refresh_page()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_public')
    @allure.title("public case-添加 content 种类")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_add_content_relate(self, go_to_content_page):
        if len(self.content_page.get_content_categories_list()) == 0:
            self.content_page.new_content_category("test-debug")

    @allure.feature('MDM_public')
    @allure.title("public case-添加 content 文件")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_add_content_file(self, go_to_content_page):
        file_path = conf.project_path + "\\Param\\Content\\"
        content_name_list = self.content_page.get_content_list()

        for test_file in test_yml["Content_info"].values():
            for file_name in test_file:
                if file_name not in content_name_list:
                    if "file" in file_name:
                        print(file_path + file_name)
                        self.content_page.add_content_file("normal_file", file_path + file_name)
                    elif "bootanimation" in file_name:
                        self.content_page.add_content_file("boot_animation", file_path + file_name)
                    elif "background" in file_name:
                        self.content_page.add_content_file("wallpaper", file_path + file_name)
                    elif "logo" in file_name:
                        self.content_page.add_content_file("logo", file_path + file_name)

    @allure.feature('MDM_public')
    @allure.title("public case-推送壁纸--请在附件查看壁纸截图效果")
    def test_release_wallpaper(self, unlock_screen, del_all_content_release_logs):
        # "All Files" "Normal Files" "Boot Animations" "Wallpaper" "LOGO"
        print("*******************推送壁纸用例开始***************************")
        log.info("*******************推送壁纸用例开始***************************")
        self.android_mdm_page.back_to_home()
        self.android_mdm_page.time_sleep(3)
        base_directory = "Wallpaper"
        org_wallpaper = "%s\\org_wallpaper.jpg" % base_directory
        self.android_mdm_page.save_screenshot_to(org_wallpaper)
        self.android_mdm_page.upload_image_JPG(
            conf.project_path + "\\ScreenShot\\%s" % org_wallpaper, "original_wallpaper")
        wallpapers = test_yml["Content_info"]["wallpaper"]
        i = 0
        for paper in wallpapers:
            i += 1
            opt_case.check_single_device(self.device_sn)
            self.content_page.go_to_new_address("content")
            file_path = conf.project_path + "\\Param\\Content\\%s" % paper
            file_size = self.content_page.get_file_size_in_windows(file_path)
            print("获取到的文件 的size(bytes): ", file_size)
            file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % paper, directory="Content")
            print("file_hash_value:", file_hash_value)
            send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                case_pack.time.localtime(self.content_page.get_current_time()))
            self.content_page.time_sleep(10)
            self.content_page.search_content('Wallpaper', paper)
            release_info = {"sn": self.device_sn, "content_name": paper}
            self.content_page.time_sleep(3)
            if len(self.content_page.get_content_list()) == 1:
                self.content_page.release_content_file(self.device_sn)
                # check release log
                self.content_page.go_to_new_address("content/release")
                self.content_page.time_sleep(3)
                now_time = self.content_page.get_current_time()
                while True:
                    release_len = len(self.content_page.get_content_latest_release_log_list(send_time, release_info))
                    print("release_len", release_len)
                    if release_len == 1:
                        break
                    elif release_len > 1:
                        assert False, "@@@@推送一次壁纸，有多条释放记录，请检查！！！"
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                        assert False, "@@@@没有相应的壁纸 release log， 请检查！！！"
                    self.content_page.time_sleep(3)
                    self.content_page.refresh_page()

                # check upgrade log
                # check if the upgrade log appeared, if appeared, break
                self.content_page.go_to_new_address("content/log")
                now_time = self.content_page.get_current_time()
                while True:
                    release_len = len(self.content_page.get_content_latest_upgrade_log(send_time, release_info))
                    if release_len == 1:
                        break
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                        assert False, "@@@@没有相应的 upgrade log， 请检查！！！"
                    self.content_page.time_sleep(5)
                    self.content_page.refresh_page()

                # check the app action in app upgrade logs, if download complete or upgrade complete, break
                now_time = self.content_page.get_current_time()
                while True:
                    upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        print(action)
                        if self.content_page.get_action_status(action) == 2 or self.content_page.get_action_status(
                                action) == 7:
                            # check the app size in device, check if app download fully
                            if not self.android_mdm_page.download_file_is_existed(paper):
                                assert False, "@@@@平台显示下载完整， 终端查询不存在此文件， 请检查！！！！"
                            size = self.android_mdm_page.get_file_size_in_device(paper)
                            print("终端下载后的的size大小：", size)
                            assert file_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                            assert file_hash_value == self.android_mdm_page.calculate_sha256_in_device(paper)
                            break
                    # wait 20 min
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 1800):
                        assert False, "@@@@20分钟还没有下载完相应的文件， 请检查！！！"
                    self.content_page.time_sleep(5)
                    self.content_page.refresh_page()

                # check upgrade
                now_time = self.content_page.get_current_time()
                while True:
                    upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        print("action", action)
                        if self.content_page.get_action_status(action) == 7:
                            break
                    # wait upgrade 3 min at most
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 180):
                        assert False, "@@@@3分钟还没有设置完相应的壁纸， 请检查！！！"
                    self.content_page.time_sleep(5)
                    self.content_page.refresh_page()

                wallpaper_before_reboot = "%s\\wallpaper.jpg" % base_directory
                self.android_mdm_page.save_screenshot_to(wallpaper_before_reboot)
                self.android_mdm_page.upload_image_JPG(
                    conf.project_path + "\\ScreenShot\\%s" % wallpaper_before_reboot,
                    "wallpaper_before_reboot-%s" % str(i))
                self.android_mdm_page.reboot_device(self.wifi_ip)
                wallpaper_after_reboot = "%s\\wallpaper_after_reboot.jpg" % base_directory
                self.android_mdm_page.save_screenshot_to(wallpaper_after_reboot)
                self.android_mdm_page.upload_image_JPG(
                    conf.project_path + "\\ScreenShot\\%s" % wallpaper_after_reboot,
                    "wallpaper_after_reboot-%s" % str(i))
            else:
                assert False, "@@@@平台上没有该壁纸： %s, 请检查" % paper

    @allure.feature('MDM_public')
    @allure.title("public case-应用满屏推送--请在附件查看满屏截图效果")
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_full_screen(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page,
                                     uninstall_multi_apps):
        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        print("*******************应用满屏推送用例开始***************************")
        log.info("*******************应用满屏推送用例开始***************************")
        file_path = self.app_page.get_apk_path(release_info["package_name"])
        package = self.app_page.get_apk_package_name(file_path)
        release_info["package"] = package
        print("包名：", package)
        version = self.app_page.get_apk_package_version(file_path)
        release_info["version"] = version

        self.android_mdm_page.uninstall_app(release_info["package"])
        self.android_mdm_page.reboot_device(self.wifi_ip)
        # check if device is online
        self.app_page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])

        app_size = self.app_page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        # check file hash value in directory Param/package
        act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_apk_package_hash_value)
        # go to app page
        self.app_page.go_to_new_address("apps")
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.app_page.get_current_time()))
        self.app_page.time_sleep(4)
        self.app_page.search_app_by_name(release_info["package_name"])
        app_list = self.app_page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.app_page.click_release_app_btn()
        self.app_page.input_release_app_info(release_info, kiosk_mode=True)

        now_time = self.app_page.get_current_time()
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
        print("**********************下载记录检测完毕*************************************")
        # check if download completed
        now_time = self.app_page.get_current_time()
        original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % release_info["package_name"])
        print("original hash value: %s" % original_hash_value)
        while True:
            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
            print("shell_hash_value: %s" % original_hash_value)
            if original_hash_value == shell_hash_value:
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
            self.app_page.time_sleep(5)
        print("**********************下载完成检测完毕*************************************")

        now_time = self.app_page.get_current_time()
        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                break
            # wait upgrade 3 min at most
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.app_page.time_sleep(1)
        print("**********************终端安装完毕*************************************")

        self.app_page.time_sleep(5)

        self.app_page.go_to_new_address("apps/logs")
        now_time = self.app_page.get_current_time()
        while True:
            upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.app_page.get_action_status(action) == 4:
                    break
            # wait upgrade 3 min at most
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.app_page.time_sleep(30)
            self.app_page.refresh_page()
        self.app_page.time_sleep(5)

        print("*******************静默安装完成***************************")
        log.info("*******************静默安装完成***************************")

        self.android_mdm_page.confirm_app_is_running(release_info["package"])
        base_directory = "APP_Full_Screen"
        image_before_reboot = "%s\\app_full_screen_before_reboot.jpg" % base_directory
        self.android_mdm_page.save_screenshot_to(image_before_reboot)
        self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_before_reboot,
                                               "app_full_screen_before_reboot")
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.confirm_app_start(release_info["package"])
        image_after_reboot = "%s\\app_full_screen_after_reboot.jpg" % base_directory
        self.android_mdm_page.confirm_app_is_running(release_info["package"])
        self.android_mdm_page.save_screenshot_to(image_after_reboot)
        self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_after_reboot,
                                               "app_full_screen_after_reboot")
        self.android_mdm_page.stop_app(release_info["package"])

    @allure.feature('MDM_public')
    @allure.title("public case-推送text.zip文件")
    def test_release_normal_files(self, unlock_screen, del_all_content_release_logs):
        # "All Files" "Normal Files" "Boot Animations" "Wallpaper" "LOGO"
        print("*******************推送文件用例开始***************************")
        log.info("*******************推送文件用例开始***************************")
        animations = test_yml["Content_info"]["normal_file"]
        # if the file is existed, delete it
        release_to_path = "%s/aimdm" % self.android_mdm_page.get_internal_storage_directory()
        grep_cmd = "ls %s" % release_to_path
        for animation in animations:
            if animation in self.android_mdm_page.u2_send_command(grep_cmd):
                self.android_mdm_page.rm_file("%s/%s" % (release_to_path, animation))
            opt_case.check_single_device(self.device_sn)
            self.content_page.go_to_new_address("content")
            file_path = conf.project_path + "\\Param\\Content\\%s" % animation
            file_size = self.content_page.get_file_size_in_windows(file_path)
            print("获取到的文件 的size(bytes): ", file_size)
            file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s " % animation, directory="Content")
            print("file_hash_value:", file_hash_value)
            send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                case_pack.time.localtime(self.content_page.get_current_time()))
            self.content_page.time_sleep(4)
            self.content_page.search_content('Normal Files', animation)
            release_info = {"sn": self.device_sn, "content_name": animation}
            self.content_page.time_sleep(3)
            assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有相关文件： %s, 请检查" % animation
            self.content_page.release_content_file(self.device_sn, file_path=release_to_path)

            # check release log
            # self.content_page.go_to_new_address("content/release")
            # self.content_page.time_sleep(3)
            # now_time = self.content_page.get_current_time()
            # while True:
            #     release_len = len(self.content_page.get_content_latest_release_log_list(send_time, release_info))
            #     print("release_len", release_len)
            #     if release_len == 1:
            #         break
            #     elif release_len > 1:
            #         assert False, "@@@@推送一次文件，有多条释放记录，请检查！！！"
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
            #         assert False, "@@@@没有相应的文件 release log， 请检查！！！"
            #     self.content_page.time_sleep(3)
            #     self.content_page.refresh_page()

            # check upgrade log
            # check if the upgrade log appeared, if appeared, break
            # self.content_page.go_to_new_address("content/log")
            # now_time = self.content_page.get_current_time()
            # while True:
            #     release_len = len(self.content_page.get_content_latest_upgrade_log(send_time, release_info))
            #     if release_len == 1:
            #         break
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
            #         assert False, "@@@@没有相应文件的 upgrade log， 请检查！！！"
            #     self.content_page.time_sleep(5)
            #     self.content_page.refresh_page()

            # check the app action in app upgrade logs, if download complete or upgrade complete, break
            # now_time = self.content_page.get_current_time()
            # while True:
            #     upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
            #     if len(upgrade_list) != 0:
            #         action = upgrade_list[0]["Action"]
            #         print(action)
            #         if self.content_page.get_action_status(action) == 2 or self.content_page.get_action_status(
            #                 action) == 7:
            #             # check the app size in device, check if app download fully
            #             if not self.android_mdm_page.download_file_is_existed(animation):
            #                 assert False, "@@@@平台显示下载完整， 终端查询不存在此文件， 请检查！！！！"
            #             size = self.android_mdm_page.get_file_size_in_device(animation)
            #             print("终端下载后的的size大小：", size)
            #             assert file_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
            #             hash_value = self.android_mdm_page.calculate_sha256_in_device(animation)
            #             assert hash_value == file_hash_value, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
            #             break
            #     # wait 20 min
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 1800):
            #         assert False, "@@@@20分钟还没有下载完相应的文件， 请检查！！！"
            #     self.content_page.time_sleep(5)
            #     self.content_page.refresh_page()

            # check upgrade
            # now_time = self.content_page.get_current_time()
            # while True:
            #     upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
            #     if len(upgrade_list) != 0:
            #         action = upgrade_list[0]["Action"]
            #         print("action", action)
            #         if self.content_page.get_action_status(action) == 7:
            #             break
            #     # wait upgrade 3 min at most
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 180):
            #         assert False, "@@@@3分钟还没有设置完相应的文件， 请检查！！！"
            #     self.content_page.time_sleep(5)
            #     self.content_page.refresh_page()

            now_time = self.content_page.get_current_time()
            while True:
                if self.android_mdm_page.download_file_is_existed(animation):
                    break
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                    assert False, "@@@@没有相应的下载记录， 请检查！！！"
                self.content_page.time_sleep(5)
            print("*************************************文件下载记录检测完毕**************************************")
            now_time = self.content_page.get_current_time()
            while True:
                if file_hash_value == self.android_mdm_page.calculate_sha256_in_device(animation):
                    break
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 900):
                    assert False, "@@@@超过15分钟还没有下载完毕，请检查！！！"
                self.content_page.time_sleep(5)
            print("*************************************文件下载完毕**************************************")
            self.content_page.go_to_new_address("content/log")
            now_time = self.content_page.get_current_time()
            while True:
                upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                if len(upgrade_list) != 0:
                    action = upgrade_list[0]["Action"]
                    print("action", action)
                    if self.content_page.get_action_status(action) == 7:
                        break
                # wait upgrade 3 min at most
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 180):
                    print(upgrade_list)
                    assert False, "@@@@3分钟还没有设置完相应的开机logo， 请检查！！！"
                self.content_page.time_sleep(5)
                self.content_page.refresh_page()

            assert animation in self.android_mdm_page.u2_send_command(
                grep_cmd), "@@@@文件没有释放到设备指定的路径%s, 请检查！！！" % release_to_path

    @allure.feature('MDM_public')
    @allure.title("public case-多应用推送")
    def test_release_multi_apps(self, del_all_app_release_log, del_download_apk, uninstall_multi_apps):
        print("*******************多应用推送用例开始***************************")
        log.info("*******************多应用推送用例开始***************************")
        release_info = {"sn": self.device_sn, "silent": "Yes", "download_network": "NO Limit", "version": False}
        apks = [test_yml["app_info"][apk_name] for apk_name in test_yml["app_info"] if
                apk_name not in ["high_version_app", "low_version_app"]]
        apks = list(set(apks))
        print(apks)
        self.app_page.go_to_new_address("apps/releases")
        self.app_page.delete_all_app_release_log()
        # self.android_mdm_page.uninstall_multi_apps()

        apks_packages = [self.android_mdm_page.get_apk_package_name(self.android_mdm_page.get_apk_path(apk)) for apk in
                         apks]
        apks_versions = [self.android_mdm_page.get_apk_package_version(self.android_mdm_page.get_apk_path(apk)) for apk
                         in apks]

        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.app_page.refresh_page()

        # check if device is online
        self.app_page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # go to app page and release multi apps one by one
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.app_page.get_current_time()))
        self.app_page.time_sleep(5)
        flag = -1
        for release_app in apks:
            flag += 1
            self.app_page.go_to_new_address("apps")
            self.app_page.search_app_by_name(release_app)
            app_list = self.app_page.get_apps_text_list()
            if len(app_list) == 0:
                assert False, "@@@@没有 %s, 请检查！！！" % release_app
            self.app_page.click_release_app_btn()
            self.app_page.input_release_app_info(release_info)

        # go to app release log
        # self.app_page.go_to_new_address("apps/releases")
        # now_time = self.app_page.get_current_time()
        # while True:
        #     if self.app_page.get_current_app_release_log_total() == len(apks_packages):
        #         break
        #     if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
        #         assert False, "@@@@超过3分钟没有相应的 app release log， 请检查！！！"
        #     self.app_page.time_sleep(3)
        #
        # print("**********************释放log检测完毕*************************************")

        # check the app download record in device
        downloading_apks = []
        now_time = self.app_page.get_current_time()
        while True:
            for d_record in range(len(apks_packages)):
                if apks[d_record] not in downloading_apks:
                    # check if app in download list
                    shell_app_apk_name = apks_packages[d_record] + "_%s.apk" % apks_versions[d_record]
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        downloading_apks.append(apks_packages[d_record])
            if len(downloading_apks) == len(apks_packages):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                diff_list = [package for package in apks_packages if package not in downloading_apks]
                download_record = ",".join(diff_list)
                assert False, "@@@@多应用推送中超过30分钟还没有%s的下载记录" % download_record
        print("**********************下载记录检测完毕*************************************")

        # check if app download completed in the settings time
        # file_path = conf.project_path + "\\Param\\Package\\"
        download_completed_apks = []
        now_time = self.app_page.get_current_time()
        while True:
            for d_completed in range(len(apks_packages)):
                if apks_packages[d_completed] not in download_completed_apks:
                    # check the app hash value in Param/Package and aimdm/download list
                    shell_app_apk_name = apks_packages[d_completed] + "_%s.apk" % apks_versions[d_completed]
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % apks[d_completed])
                    if original_hash_value == shell_hash_value:
                        download_completed_apks.append(apks_packages[d_completed])
            if len(download_completed_apks) == len(apks_packages):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                diff_list = [package for package in apks_packages if package not in download_completed_apks]
                download_missing_record = ",".join(diff_list)
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % download_missing_record
        print("已经下载完的app： ", download_completed_apks)

        print("**********************下载完成检测完毕*************************************")

        # check if app installed in settings time
        now_time = self.app_page.get_current_time()
        installed_apks = []
        while True:
            for d_installed in range(len(apks_packages)):
                # check if app in download list
                if apks_packages[d_installed] not in installed_apks:
                    if self.android_mdm_page.app_is_installed(apks_packages[d_installed]):
                        installed_apks.append(apks_packages[d_installed])
                        print(installed_apks)
            if len(installed_apks) == len(apks_packages):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                diff_list = [package for package in apks_packages if package not in installed_apks]
                uninstalled_record = ",".join(diff_list)
                print(uninstalled_record)
                assert False, "@@@@多应用推送中超过3分钟还没有%s的安装记录" % uninstalled_record
        print("******************************安装记录检测完毕****************************************")

        # check if all installed success logs in app upgrade logs
        self.app_page.go_to_new_address("apps/logs")
        report_installed = []
        now_time = self.app_page.get_current_time()
        while True:
            flag = -1
            for installed_app in apks_packages:
                flag += 1
                if installed_app not in report_installed:
                    self.app_page.search_upgrade_logs(installed_app, self.device_sn)
                    release_info["package"] = installed_app
                    release_info["version"] = self.android_mdm_page.get_apk_package_version(
                        self.android_mdm_page.get_apk_path(apks[flag]))
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        print(action)
                        if self.app_page.get_action_status(action) == 4:
                            report_installed.append(installed_app)
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        assert False, "@@@@设备已经安装完相应的， 请检查！！！"
                    self.app_page.time_sleep(3)
                    self.app_page.refresh_page()
            if len(report_installed) == len(apks_packages):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                diff_list = [package for package in apks_packages if package not in report_installed]
                uninstalled_report = ",".join(diff_list)
                assert False, "@@@@多应用推送中设备已经安装完毕所有的app, 平套超过5分钟还上报%s的安装记录" % uninstalled_report

    @allure.feature('MDM_public')
    @allure.title("public case- 静默升级系统app")
    def test_upgrade_system_app(self, del_all_app_release_log, del_download_apk, uninstall_system_app):
        print("*******************静默升级系统app用例开始***************************")
        log.info("*******************静默升级系统app用例开始***************************")
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit", "auto_open": "YES"}
        file_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
        #
        # # install low version system application
        # # set app as system app
        self.android_mdm_page.wifi_adb_root(self.wifi_ip)
        assert not self.android_mdm_page.app_is_installed(
            self.android_mdm_page.get_apk_package_name(file_path))
        # push file to system/app
        self.android_mdm_page.push_file_to_device(
            self.android_mdm_page.get_apk_path(test_yml['app_info']['low_version_app']), "/system/app/")
        print(self.android_mdm_page.u2_send_command("ls /system/app"))
        #
        self.android_mdm_page.reboot_device(self.wifi_ip)
        assert self.android_mdm_page.app_is_installed(
            self.android_mdm_page.get_apk_package_name(file_path)), "@@@没有安装系统应用， 请检查！！！！"

        # release high version system app
        package = self.app_page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.app_page.get_apk_package_version(file_path)
        release_info["version"] = version
        # check if device is online
        self.app_page.go_to_new_address("devices")
        opt_case.check_single_device(release_info["sn"])
        # app_size_mdm = self.page.get_app_size()  for web
        # check app size(bytes) in windows
        app_size = self.app_page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)

        # go to app page
        self.app_page.go_to_new_address("apps")
        self.app_page.search_app_by_name(release_info["package_name"])
        app_list = self.app_page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.app_page.get_current_time()))
        self.app_page.time_sleep(10)
        self.app_page.click_release_app_btn()
        self.app_page.input_release_app_info(release_info)
        # go to app release log
        # self.app_page.go_to_new_address("apps/releases")
        # # self.page.check_release_log_info(send_time, release_info["sn"])
        #
        # now_time = self.app_page.get_current_time()
        # # print(self.page.get_app_current_release_log_list(send_time, release_info["sn"]))
        # while True:
        #     release_len = len(self.app_page.get_app_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
        #     if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app release log， 请检查！！！"
        #     self.app_page.time_sleep(1)
        #     self.app_page.refresh_page()
        #
        # # check if the upgrade log appeared, if appeared, break
        # self.app_page.go_to_new_address("apps/logs")
        # now_time = self.app_page.get_current_time()
        # while True:
        #     release_len = len(self.app_page.get_app_latest_upgrade_log(send_time, release_info))
        #     if release_len == 1:
        #         break
        #     if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
        #     self.app_page.time_sleep(3)
        #     self.app_page.refresh_page()
        #
        # # check the app action in app upgrade logs, if download complete or upgrade complete, break
        # now_time = self.app_page.get_current_time()
        # while True:
        #     upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         if self.app_page.get_action_status(action) == 2 or self.app_page.get_action_status(action) == 4 \
        #                 or self.app_page.get_action_status(action) == 3:
        #             # check the app size in device, check if app download fully
        #             shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        #             if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
        #                 assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
        #
        #             size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
        #             print("终端下载后的的size大小：", size)
        #             if app_size != size:
        #                 assert False, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #             break
        #         # wait 20 mins
        #     if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 640):
        #         assert False, "@@@@20分钟还没有下载完相应的app， 请检查！！！"
        #     self.app_page.refresh_page()
        #     self.app_page.time_sleep(5)
        #
        # # check upgrade
        # now_time = self.app_page.get_current_time()
        # while True:
        #     upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print("action", action)
        #         if self.app_page.get_action_status(action) == 4:
        #             if self.android_mdm_page.app_is_installed(release_info["package"]):
        #                 version_installed = self.app_page.transfer_version_into_int(
        #                     self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
        #                 if version_installed == self.app_page.transfer_version_into_int(release_info["version"]):
        #                     break
        #                 else:
        #                     assert False, "@@@@平台显示已经完成覆盖安装了app, 终端发现没有安装高版本的app，还是原来的版本， 请检查！！！！"
        #     # wait upgrade 3 mins at most
        #     if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
        #         assert False, "@@@@3分钟还没有静默安装完相应的app， 请检查！！！"
        #     self.app_page.refresh_page()
        #     self.app_page.time_sleep(5)

        now_time = self.app_page.get_current_time()
        shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                assert False, "@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
        print("**********************下载记录检测完毕*************************************")

        # check if download completed
        now_time = self.app_page.get_current_time()
        original_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % release_info["package_name"])
        print("original hash value: %s" % original_hash_value)
        while True:
            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
            print("shell_hash_value: %s" % original_hash_value)
            if original_hash_value == shell_hash_value:
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
            self.app_page.time_sleep(60)
        print("**********************下载完成检测完毕*************************************")

        while True:
            if self.android_mdm_page.app_is_installed(release_info["package"]):
                version_installed = self.app_page.transfer_version_into_int(
                    self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                if version_installed == self.app_page.transfer_version_into_int(release_info["version"]):
                    break
                else:
                    assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
            self.app_page.time_sleep(1)
        self.app_page.time_sleep(5)
        print("**********************终端成功安装app*************************************")

        self.app_page.go_to_new_address("apps/logs")
        self.app_page.refresh_page()
        now_time = self.app_page.get_current_time()
        while True:
            upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                break
            # wait upgrade 3 min at most
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
            self.app_page.time_sleep(60)
            self.app_page.refresh_page()
        self.app_page.time_sleep(5)

        try:
            self.android_mdm_page.confirm_app_is_running(release_info["package"])
        except AttributeError:
            print("app 推送选择了安装完成后自动运行app, app安装完后2分钟内还没自动运行")
        self.android_mdm_page.stop_app(release_info["package"])
        self.android_mdm_page.rm_file("system/app/%s" % test_yml['app_info']['low_version_app'])

    @allure.feature('MDM_public1')
    @allure.title("public case- 静默ota升级")
    def test_silent_ota_upgrade(self, del_all_ota_release_log, go_to_ota_page, delete_ota_package_relate):
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        self.android_mdm_page.del_updated_zip()
        release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
        current_firmware_version = self.android_mdm_page.check_firmware_version()
        # compare current version and exp version
        assert self.ota_page.transfer_version_into_int(
            current_firmware_version) < self.ota_page.transfer_version_into_int(
            release_info["version"]), \
            "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"

        # reboot
        self.android_mdm_page.reboot_device(self.wifi_ip)
        # search package

        device_current_firmware_version = self.android_mdm_page.check_firmware_version()
        print("设备当前固件版本：%s" % device_current_firmware_version)
        log.info("设备当前固件版本：%s" % device_current_firmware_version)
        print("ota after upgrade version:", release_info["version"])
        ota_package_size = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
        act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        act_ota_package_size = self.ota_page.get_zip_size(ota_package_size)
        print("act_ota_package_size:", act_ota_package_size)
        self.ota_page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.Page.get_package_ele(release_info["package_name"])
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.ota_page.get_current_time()))
        print("send_time", send_time)
        self.ota_page.time_sleep(10)
        # if device is existed, click
        self.ota_page.click_release_btn()
        self.ota_page.input_release_OTA_package(release_info, is_silent=True)

        # check download record in device
        now_time = self.ota_page.get_current_time()
        while True:
            # check if app in download list
            if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                break
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]
            self.ota_page.time_sleep(10)

        upgrade_flag = 0
        now_time = self.ota_page.get_current_time()
        while True:
            info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
            if len(info) != 0:
                action = info[0]["Action"]
                print("action", action)
                if self.ota_page.get_action_status(action) in [2, 3, 4]:
                    if action == 4:
                        upgrade_flag = 1
                    break
            # wait upgrade 3 mins at most
            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                assert False, "@@@@30分钟还没有下载完相应的固件， 请检查！！！"
            self.ota_page.time_sleep(30)
            self.ota_page.refresh_page()
        print("************************下载完成*************************************")
        # now_time = self.ota_page.get_current_time()
        # while True:
        #     download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
        #     package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
        #     if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
        #         print("原来升级包的 package_hash_value：", package_hash_value)
        #         print("下载完成后的 package_hash_value：", act_ota_package_hash_value)
        #         log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
        #         log.info("下载完成后的 package_hash_value：%s" % str(act_ota_package_hash_value))
        #         break
        #
        #     if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 1200):
        #         err_msg = "@@@@20分钟后还没有下载完相应的ota package， 请检查！！！"
        #         log.error(err_msg)
        #         print(err_msg)
        #         assert False, err_msg
        #     self.ota_page.time_sleep(10)

        # check upgrade
        if upgrade_flag == 0:
            now_time = self.ota_page.get_current_time()
            while True:
                info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                if len(info) != 0:
                    action = info[0]["Action"]
                    print("action", action)
                    if self.ota_page.get_action_status(action) == 4:
                        break
                # wait upgrade 3 mins at most
                if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                    assert False, "@@@@30分钟还没有升级相应的安卓版本， 请检查！！！"
                self.ota_page.time_sleep(30)
                self.ota_page.refresh_page()
        print("************************平台显示升级完成完成*************************************")

        self.android_mdm_page.device_boot(self.wifi_ip)
        after_upgrade_version = self.android_mdm_page.check_firmware_version()
        print("设备升级后的固件版本：%s" % after_upgrade_version)
        log.info("设备升级后的固件版本：%s" % after_upgrade_version)
        assert self.ota_page.transfer_version_into_int(
            device_current_firmware_version) != self.ota_page.transfer_version_into_int(after_upgrade_version), \
            "@@@@ota升级失败， 还是原来的版本%s！！" % device_current_firmware_version
        assert self.ota_page.transfer_version_into_int(release_info["version"]) == \
               self.ota_page.transfer_version_into_int(
                   after_upgrade_version), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
        print("************************静默ota升级完成升级完成完成*************************************")

    @allure.feature('MDM_public')
    @allure.title("public case-推送开机logo/动画")
    def test_release_boot_logo_and_animation(self, unlock_screen, del_all_content_release_logs):
        # "All Files" "Normal Files" "Boot Animations" "Wallpaper" "LOGO"
        print("*******************推送开机logo/动画开始***************************")
        log.info("*******************推送开机logo/动画开始***************************")
        logos = test_yml["Content_info"]["boot_logo"]
        animation = test_yml["Content_info"]["boot_animation"][0]

        opt_case.check_single_device(self.device_sn)
        self.content_page.go_to_new_address("content")
        file_path = conf.project_path + "\\Param\\Content\\%s" % animation
        file_size = self.content_page.get_file_size_in_windows(file_path)
        print("获取到的文件 的size(bytes): ", file_size)
        file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s " % animation, directory="Content")
        print("file_hash_value:", file_hash_value)
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.content_page.get_current_time()))
        self.content_page.time_sleep(4)
        self.content_page.search_content('Boot Animations', animation)
        release_info = {"sn": self.device_sn, "content_name": animation}
        self.content_page.time_sleep(3)
        assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有机动画： %s, 请检查" % animation
        self.content_page.release_content_file(self.device_sn)
        # check release log
        # self.content_page.go_to_new_address("content/release")
        # self.content_page.time_sleep(3)
        # now_time = self.content_page.get_current_time()
        # while True:
        #     release_len = len(self.content_page.get_content_latest_release_log_list(send_time, release_info))
        #     print("release_len", release_len)
        #     if release_len == 1:
        #         break
        #     elif release_len > 1:
        #         assert False, "@@@@推送一次机动画，有多条释放记录，请检查！！！"
        #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的机动画 release log， 请检查！！！"
        #     self.content_page.time_sleep(3)
        #     self.content_page.refresh_page()

        # check upgrade log
        # check if the upgrade log appeared, if appeared, break

        now_time = self.content_page.get_current_time()
        while True:
            if self.android_mdm_page.download_file_is_existed(animation):
                break
            if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                assert False, "@@@@没有相应的下载记录， 请检查！！！"
            self.content_page.time_sleep(5)
        print("*************************************文件下载记录检测完毕**************************************")
        now_time = self.content_page.get_current_time()
        while True:
            if file_hash_value == self.android_mdm_page.calculate_sha256_in_device(animation):
                break
            if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 900):
                assert False, "@@@@超过15分钟还没有下载完毕，请检查！！！"
            self.content_page.time_sleep(5)

        # self.content_page.go_to_new_address("content/log")
        # now_time = self.content_page.get_current_time()
        # while True:
        #     release_len = len(self.content_page.get_content_latest_upgrade_log(send_time, release_info))
        #     if release_len == 1:
        #         break
        #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
        #         assert False, "@@@@没有相应的 upgrade log， 请检查！！！"
        #     self.content_page.time_sleep(5)
        #     self.content_page.refresh_page()

        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        # now_time = self.content_page.get_current_time()
        # while True:
        #     upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
        #     if len(upgrade_list) != 0:
        #         action = upgrade_list[0]["Action"]
        #         print(action)
        #         if self.content_page.get_action_status(action) == 2 or self.content_page.get_action_status(
        #                 action) == 7:
        #             # check the app size in device, check if app download fully
        #             if not self.android_mdm_page.download_file_is_existed(animation):
        #                 assert False, "@@@@平台显示下载完整， 终端查询不存在此文件， 请检查！！！！"
        #             size = self.android_mdm_page.get_file_size_in_device(animation)
        #             print("终端下载后的的size大小：", size)
        #             assert file_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #             assert file_hash_value == self.android_mdm_page.calculate_sha256_in_device(
        #                 animation), "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
        #             break
        #     # wait 20 min
        #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 1800):
        #         assert False, "@@@@20分钟还没有下载完相应的文件， 请检查！！！"
        #     self.content_page.time_sleep(5)
        #     self.content_page.refresh_page()

        # check upgrade
        self.content_page.go_to_new_address("content/log")
        now_time = self.content_page.get_current_time()
        while True:
            upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.content_page.get_action_status(action) == 7:
                    break
            # wait upgrade 3 min at most
            if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有设置完相应的开机动画， 请检查！！！"
            self.content_page.time_sleep(30)
            self.content_page.refresh_page()
        print(
            "*****************************************动画推送完成*********************************************************")
        # release logo
        i = 0
        for logo in logos:
            i += 1
            opt_case.check_single_device(self.device_sn)
            self.content_page.go_to_new_address("content")
            file_path = conf.project_path + "\\Param\\Content\\%s" % logo
            file_size = self.content_page.get_file_size_in_windows(file_path)
            print("获取到的文件 的size(bytes): ", file_size)
            send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                case_pack.time.localtime(self.content_page.get_current_time()))
            self.content_page.time_sleep(4)
            self.content_page.search_content('LOGO', logo)
            release_info = {"sn": self.device_sn, "content_name": logo}
            self.content_page.time_sleep(3)
            assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有该logo图片： %s, 请检查" % logo
            self.content_page.release_content_file(self.device_sn)
            # check release log
            # self.content_page.go_to_new_address("content/release")
            # self.content_page.time_sleep(3)
            # now_time = self.content_page.get_current_time()
            # while True:
            #     release_len = len(self.content_page.get_content_latest_release_log_list(send_time, release_info))
            #     print("release_len", release_len)
            #     if release_len == 1:
            #         break
            #     elif release_len > 1:
            #         assert False, "@@@@推送一次开机logo，有多条释放记录，请检查！！！"
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
            #         assert False, "@@@@没有相应的开机logo release log， 请检查！！！"
            #     self.content_page.time_sleep(3)
            #     self.content_page.refresh_page()
            #
            # # check upgrade log
            # # check if the upgrade log appeared, if appeared, break
            # self.content_page.go_to_new_address("content/log")
            # now_time = self.content_page.get_current_time()
            # while True:
            #     release_len = len(self.content_page.get_content_latest_upgrade_log(send_time, release_info))
            #     if release_len == 1:
            #         break
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
            #         assert False, "@@@@没有相应的 upgrade log， 请检查！！！"
            #     self.content_page.time_sleep(5)
            #     self.content_page.refresh_page()
            #
            # # check the app action in app upgrade logs, if download complete or upgrade complete, break
            # now_time = self.content_page.get_current_time()
            # while True:
            #     upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
            #     if len(upgrade_list) != 0:
            #         action = upgrade_list[0]["Action"]
            #         print(action)
            #         if self.content_page.get_action_status(action) == 2 or self.content_page.get_action_status(
            #                 action) == 7:
            #             # check the app size in device, check if app download fully
            #             if not self.android_mdm_page.download_file_is_existed(logo):
            #                 assert False, "@@@@平台显示下载完整， 终端查询不存在此文件， 请检查！！！！"
            #             size = self.android_mdm_page.get_file_size_in_device(logo)
            #             print("终端下载后的的size大小：", size)
            #             assert file_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
            #             break
            #     # wait 20 min
            #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 1800):
            #         assert False, "@@@@20分钟还没有下载完相应的文件， 请检查！！！"
            #     self.content_page.time_sleep(5)
            #     self.content_page.refresh_page()

            # check upgrade

            now_time = self.content_page.get_current_time()
            while True:
                if self.android_mdm_page.download_file_is_existed(logo):
                    break
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                    assert False, "@@@@没有相应的下载记录， 请检查！！！"
                self.content_page.time_sleep(5)
            print("*************************************文件下载记录检测完毕**************************************")
            now_time = self.content_page.get_current_time()
            while True:
                if file_hash_value == self.android_mdm_page.calculate_sha256_in_device(animation):
                    break
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 900):
                    assert False, "@@@@超过15分钟还没有下载完毕，请检查！！！"
                self.content_page.time_sleep(5)
            print("*************************************文件下载完毕**************************************")
            self.content_page.go_to_new_address("content/log")
            now_time = self.content_page.get_current_time()
            while True:
                upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                if len(upgrade_list) != 0:
                    action = upgrade_list[0]["Action"]
                    print("action", action)
                    if self.content_page.get_action_status(action) == 7:
                        break
                # wait upgrade 3 min at most
                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 180):
                    assert False, "@@@@3分钟还没有设置完相应的开机logo， 请检查！！！"
                self.content_page.time_sleep(5)
                self.content_page.refresh_page()

            # case_pack.AlertData().getAlert("请关掉提示框并且查看启动logo和动画")
            self.android_mdm_page.reboot_device(self.wifi_ip)
            self.content_page.time_sleep(5)

    @allure.feature('MDM_public-- no test now ')
    @allure.title("public case-无线休眠推送app")
    def test_report_device_sleep_status(self, del_all_app_release_log,
                                        del_all_app_uninstall_release_log, go_to_device_page):
        print("*******************无线休眠推送app用例开始***************************")
        log.info("*******************无线休眠推送app用例开始***************************")
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.android_mdm_page.screen_keep_on()
        self.android_mdm_page.back_to_home()
        # self.android_mdm_page.confirm_unplug_usb_wire()
        # case_pack.AlertData().getAlert("请拔开USB线再点击确定")

        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        file_path = self.app_page.get_apk_path(release_info["package_name"])
        package = self.app_page.get_apk_package_name(file_path)
        release_info["package"] = package
        version = self.app_page.get_apk_package_version(file_path)
        release_info["version"] = version

        app_size = self.app_page.get_file_size_in_windows(file_path)
        print("获取到的app 的size(bytes): ", app_size)
        # check file hash value in directory Param/package
        act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
        print("act_ota_package_hash_value:", act_apk_package_hash_value)

        device_info = opt_case.check_single_device(self.device_sn)[0]
        msg = "online"
        # clear other alert
        if self.device_page.upper_transfer("on") in self.device_page.remove_space_and_upper(device_info["Status"]):
            if self.device_page.upper_transfer("Locked") in self.device_page.remove_space_and_upper(
                    device_info["Lock Status"]):
                self.device_page.select_device(self.device_sn)
                self.device_page.click_unlock()
        if self.android_mdm_page.public_alert_show(2):
            self.android_mdm_page.clear_download_and_upgrade_alert()

        self.device_page.select_device(self.device_sn)
        self.device_page.send_message(msg)
        if not self.android_mdm_page.public_alert_show(60):
            assert False, "@@@@平台显示设备在线， 发送消息一分钟后还没收到消息"
        self.android_mdm_page.confirm_received_text(msg, timeout=5)
        try:
            self.android_mdm_page.click_msg_confirm_btn()
            self.android_mdm_page.confirm_msg_alert_fade(msg)
        except Exception:
            pass

        self.android_mdm_page.device_sleep()
        self.android_mdm_page.time_sleep(test_yml["android_device_info"]["sleep_time"])
        # self.android_mdm_page.time_sleep(60)
        self.device_page.refresh_page()
        opt_case.check_single_device(self.device_sn)
        self.android_mdm_page.device_is_existed(self.wifi_ip)
        # self.device_page.select_device(self.device_sn)
        # self.device_page.send_message(msg)
        # if not self.android_mdm_page.public_alert_show(60):
        #     assert False, "@@@@平台显示设备在线， 发送消息一分钟后还没收到消息"
        # self.android_mdm_page.confirm_received_text(msg, timeout=5)
        # try:
        #     self.android_mdm_page.click_msg_confirm_btn()
        #     self.android_mdm_page.confirm_msg_alert_fade(msg)
        # except Exception:
        #     pass

        # go to app page
        self.app_page.go_to_new_address("apps")
        send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                            case_pack.time.localtime(self.app_page.get_current_time()))
        self.app_page.time_sleep(4)
        self.app_page.search_app_by_name(release_info["package_name"])
        app_list = self.app_page.get_apps_text_list()
        if len(app_list) == 0:
            assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
        self.app_page.click_release_app_btn()
        self.app_page.input_release_app_info(release_info)
        # go to app release log
        self.app_page.go_to_new_address("apps/releases")

        now_time = self.app_page.get_current_time()
        # print(self.app_page.get_app_current_release_log_list(send_time, release_info["sn"]))
        while True:
            release_len = len(self.app_page.get_app_latest_release_log_list(send_time, release_info))
            print("release_len", release_len)
            if release_len == 1:
                break
            elif release_len > 1:
                assert False, "@@@@释放一次app，有多条释放记录，请检查！！！"
            else:
                self.app_page.refresh_page()
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app release log， 请检查！！！"
            self.app_page.time_sleep(3)

        # check if the upgrade log appeared, if appeared, break
        self.app_page.go_to_new_address("apps/logs")
        now_time = self.app_page.get_current_time()
        while True:
            release_len = len(self.app_page.get_app_latest_upgrade_log(send_time, release_info))
            if release_len == 1:
                break
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
                assert False, "@@@@没有相应的 app upgrade log， 请检查！！！"
            self.app_page.time_sleep(5)
            self.app_page.refresh_page()

        """
        Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
         4: upgrading complete, 5: downloading failed, 6: upgrading failed)
         0: Uninstall completed
        """
        # check the app action in app upgrade logs, if download complete or upgrade complete, break
        now_time = self.app_page.get_current_time()
        while True:
            upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print(action)
                if self.app_page.get_action_status(action) == 2 or self.app_page.get_action_status(action) == 4 \
                        or self.app_page.get_action_status(action) == 3:
                    # check the app size in device, check if app download fully
                    shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                    if not self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@平台显示下载完apk包， 终端查询不存在此包， 请检查！！！！"
                    size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
                    print("终端下载后的的size大小：", size)
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    print("原来升级包的 package_hash_value：", act_apk_package_hash_value)
                    print("下载完成后的 package_hash_value：", package_hash_value)
                    assert app_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                    assert package_hash_value == act_apk_package_hash_value, "@@@@平台显示下载完成，终端的apk和原始的apkSHA-256值不一致， 请检查！！！！"
                    break
            # wait 20 mins
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                assert False, "@@@@30分钟还没有下载完相应的app， 请检查！！！"
            self.app_page.time_sleep(5)
            self.app_page.refresh_page()

        # check upgrade
        now_time = self.app_page.get_current_time()
        while True:
            upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
            if len(upgrade_list) != 0:
                action = upgrade_list[0]["Action"]
                print("action", action)
                if self.app_page.get_action_status(action) == 4:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    else:
                        assert False, "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
            # wait upgrade 3 min at most
            if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
            self.app_page.time_sleep(5)
            self.app_page.refresh_page()
        self.app_page.time_sleep(5)

    @allure.feature('MDM_public111')
    @allure.title("Devices- 关机 -- test in the last")
    def test_device_shutdown(self):
        print("*******************关机用例开始***************************")
        log.info("*******************关机用例开始***************************")
        sn = self.device_sn
        exp_shutdown_text = "Device ShutDown Command sent"
        opt_case.check_single_device(sn)
        self.device_page.click_dropdown_btn()
        self.device_page.click_shutdown_btn()
        # check if shutdown command works in 3 sec
        self.device_page.time_sleep(3)
        assert "%sdevice" % self.android_mdm_page.get_device_name() not in self.device_page.remove_space(
            self.android_mdm_page.devices_list()), "@@@@3s内还没触发关机， 请检查！！！"
        self.device_page.refresh_page()
        assert "Off" in opt_case.get_single_device_list(sn)[0]["Status"], "@@@@已发送关机命令， 设备还显示在线状态"
        # check device

    @allure.feature('MDM_public1111_test_test111')
    @allure.title("public case- 长时间检测设备在线情况")
    def test_test(self):
        # param = {"android_page": td, "sn": sn, "ip": ip}
        data = opt_case.check_single_device(self.device_sn)
        length = 1
        now = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(case_pack.time.time()))
        for i in range(length):
            if self.android_mdm_page.public_alert_show(3):
                self.android_mdm_page.clear_download_and_upgrade_alert()
            msg = "%s:test%d" % (now, i)
            # get thread lock
            # lock.acquire()
            self.device_page.refresh_page()
            device_info = opt_case.get_single_device_list(self.device_sn)[0]
            if self.device_page.upper_transfer("on") in self.device_page.remove_space_and_upper(
                    device_info["Status"]):
                if self.device_page.upper_transfer("Locked") in self.device_page.remove_space_and_upper(
                        device_info["Lock Status"]):
                    self.device_page.select_device(self.device_sn)
                    self.device_page.click_unlock()
                    self.device_page.refresh_page()
                self.device_page.select_device(self.device_sn)
                self.device_page.click_send_btn()
                self.device_page.msg_input_and_send(msg)
                # unlock thread
                # lock.release()
                # check message in device
                # self.android_mdm_page.screen_keep_on()
                if not self.android_mdm_page.public_alert_show(60):
                    continue
                # try:
                self.android_mdm_page.confirm_received_text(msg, timeout=5)
                # except AttributeError:
                #     continue
                # try:
                self.android_mdm_page.click_msg_confirm_btn()
                self.android_mdm_page.confirm_msg_alert_fade(msg)
                # except Exception:
                #     pass
            self.android_mdm_page.reboot_device(self.device_sn)
            if self.android_mdm_page.public_alert_show(timeout=5):
                self.android_mdm_page.clear_download_and_upgrade_alert()
            self.device_page.refresh_page()
            # get lock
            # lock.acquire()
            device_info_after_reboot = opt_case.get_single_device_list(self.device_sn)[0]
            if self.device_page.upper_transfer("on") in self.device_page.remove_space_and_upper(
                    device_info_after_reboot["Status"]):
                self.device_page.select_device(self.device_sn)
                self.device_page.click_send_btn()
                self.device_page.msg_input_and_send(msg)
                # lock.release()
                # check message in device
                # self.android_mdm_page.screen_keep_on()
                if not self.android_mdm_page.public_alert_show(60):
                    continue
                try:
                    self.android_mdm_page.confirm_received_text(msg, timeout=5)
                except AttributeError:
                    continue
                try:
                    self.android_mdm_page.click_msg_confirm_btn()
                    self.android_mdm_page.confirm_msg_alert_fade(msg)
                except Exception:
                    pass
            # online_flag += 1
            self.device_page.refresh_page()
