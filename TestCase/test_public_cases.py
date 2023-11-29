import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
test_yml = case_pack.yaml_data
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()
usb_serial = case_pack.Serial()

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


class TestPublicPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.device_page = case_pack.DevicesPage(self.driver, 40)
        self.app_page = case_pack.APPSPage(self.driver, 40)
        self.ota_page = case_pack.OTAPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.content_page = case_pack.ContentPage(self.driver, 40)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_content_file()
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.content_page.refresh_page()
        self.silent_ota_upgrade_flag = 0

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_all_content_file()
        self.app_page.refresh_page()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_public')
    @allure.title("public case-添加 content 种类--辅助测试用例")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_add_content_category(self, go_to_content_page):
        while True:
            try:
                log.info("===================添加 content 种类--辅助测试用例开始==================")
                self.content_page.refresh_page()
                if len(self.content_page.get_content_categories_list()) == 0:
                    self.content_page.new_content_category("test-debug")
                log.info("===================添加 content 种类--辅助测试用例结束==================")
                break
            except Exception as e:
                if self.device_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.go_to_new_address("content")

    @allure.feature('MDM_public')
    @allure.title("public case-添加 content 文件--辅助测试用例")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_add_content_file(self, go_to_content_page):
        while True:
            try:
                log.info("public case-添加 content 文件--辅助测试用例开始")
                self.content_page.refresh_page()
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
                log.info("public case-添加 content 文件--辅助测试用例开始结束")
                break
            except Exception as e:
                if self.device_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.go_to_new_address("content")

    @allure.feature('MDM_public')
    @allure.story('MDM-Show')
    @allure.title("public case-推送壁纸--请在附件查看壁纸截图效果")
    # @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_release_wallpaper(self, unlock_screen, del_all_content_release_logs):
        while True:
            try:
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
                    log.info("获取到的文件 的size(bytes): %s" % str(file_size))
                    file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % paper, directory="Content")
                    log.info("file_hash_value: %s" % str(file_hash_value))

                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(self.content_page.get_current_time()))
                    self.content_page.time_sleep(10)
                    self.content_page.search_content('Wallpaper', paper)
                    release_info = {"sn": self.device_sn, "content_name": paper}
                    self.content_page.time_sleep(3)
                    if len(self.content_page.get_content_list()) == 1:
                        self.content_page.release_content_file(self.device_sn)
                        log.info("推送指令下达成功")
                        # check release record in device
                        now_time = self.content_page.get_current_time()
                        while True:
                            if self.android_mdm_page.download_file_is_existed(paper):
                                log.info("终端存在壁纸：%s 的下载记录" % paper)
                                break
                            if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                                log.error("@@@@终端没有壁纸: %s的下载记录" % paper)
                                assert False, "@@@@终端没有壁纸: %s的下载记录" % paper
                            self.content_page.time_sleep(3)
                        log.info("检测upgrade log")
                        # check upgrade log
                        # check if the upgrade log appeared, if appeared, break
                        self.content_page.go_to_new_address("content/log")
                        # check the app action in app upgrade logs, if download complete or upgrade complete, break
                        download_time = self.content_page.get_current_time()
                        while True:
                            upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                            if len(upgrade_list) != 0:
                                action = upgrade_list[0]["Action"]
                                log.info("平台upgrade log状态： %s" % action)
                                if self.content_page.get_action_status(action) == 2 or self.content_page.get_action_status(
                                        action) == 7:
                                    # check the app size in device, check if app download fully
                                    size = self.android_mdm_page.get_file_size_in_device(paper)
                                    log.info("终端下载后的的size大小： %s" % str(size))
                                    assert file_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                                    log.info("壁纸前后对比大小一致")
                                    assert file_hash_value == self.android_mdm_page.calculate_sha256_in_device(paper)
                                    log.info("文件前后的hash256值一致")
                                    break
                            # wait 20 min
                            if self.content_page.get_current_time() > self.content_page.return_end_time(download_time, 1200):
                                if self.content_page.service_is_normal():
                                    log.error("@@@@20分钟还没有下载完相应的文件， 请检查！！！")
                                    assert False, "@@@@20分钟还没有下载完相应的文件， 请检查！！！"
                                else:
                                    self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                                    download_time = self.content_page.get_current_time()
                            self.content_page.time_sleep(5)
                            self.content_page.refresh_page()
                        log.info("*************************壁纸：%s 下载完毕*****************************" % paper)
                        # check upgrade
                        report_time = self.content_page.get_current_time()
                        while True:
                            upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                            if len(upgrade_list) != 0:
                                action = upgrade_list[0]["Action"]
                                log.info("平台显示的状态： %s" % action)
                                if self.content_page.get_action_status(action) == 7:
                                    log.info("平台显示已经设置完成壁纸")
                                    break
                            # wait upgrade 3 min at most
                            if self.content_page.get_current_time() > self.content_page.return_end_time(report_time, 180):
                                if self.content_page.service_is_normal():
                                    log.error("@@@@3分钟还没有设置完相应的壁纸， 请检查！！！")
                                    assert False, "@@@@3分钟还没有设置完相应的壁纸， 请检查！！！"
                                else:
                                    self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                                    report_time = self.content_page.get_current_time()
                            self.content_page.time_sleep(5)
                            self.content_page.refresh_page()
                        log.info("*************壁纸：%s 平台显示已经设置完成***********" % paper)
                        wallpaper_before_reboot = "%s\\wallpaper.jpg" % base_directory
                        self.android_mdm_page.save_screenshot_to(wallpaper_before_reboot)
                        self.android_mdm_page.upload_image_JPG(
                            conf.project_path + "\\ScreenShot\\%s" % wallpaper_before_reboot,
                            "wallpaper_before_reboot-%s" % str(i))
                        # no test tomorrow to save time
                        self.android_mdm_page.reboot_device(self.wifi_ip)
                        wallpaper_after_reboot = "%s\\wallpaper_after_reboot.jpg" % base_directory
                        self.android_mdm_page.save_screenshot_to(wallpaper_after_reboot)
                        self.android_mdm_page.upload_image_JPG(
                            conf.project_path + "\\ScreenShot\\%s" % wallpaper_after_reboot,
                            "wallpaper_after_reboot-%s" % str(i))
                    else:
                        log.error("@@@@平台上没有该壁纸： %s, 请检查" % paper)
                        assert False, "@@@@平台上没有该壁纸： %s, 请检查" % paper
                log.info("*******************推送壁纸用例结束***************************")
                break
            except Exception as e:
                if self.device_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.go_to_new_address("content")
                    self.content_page.delete_all_content_release_log()
                    self.android_mdm_page.del_all_content_file()
                    self.android_mdm_page.screen_keep_on()

    @allure.feature('MDM_public')
    @allure.story('MDM-Show')
    @allure.title("OTA-OTA重启5次断点续传")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_upgrade_OTA_package_reboot_5times(self, del_all_ota_release_log, go_to_ota_page,
                                               delete_ota_package_relate):
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        while True:
            try:
                print("*******************OTA重启5次断点续传用例开始***************************")
                log.info("*******************OTA重启5次断点续传用例开始***************************")
                # get release ota package version
                times = 2
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                assert self.ota_page.transfer_version_into_int(current_firmware_version) < self.ota_page.transfer_version_into_int(
                    release_info["version"]), \
                    "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                # reboot and sync data with platform
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # search package
                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("当前版本为： %s" % device_current_firmware_version)
                log.info("目的版本为: %s" % release_info["version"])
                # check file size and hash value in directory Param/package
                ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
                log.info("act_ota_package_size: %s" % act_ota_package_size)
                # check file hash value in directory Param/package
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
                log.info("act_ota_package_hash_value: %s" % act_ota_package_hash_value)
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(self.ota_page.get_current_time()))
                print("send_time", send_time)
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                self.ota_page.input_release_OTA_package(release_info)
                log.info("推送ota包： %s指令下达成功" % release_info["package_name"])
                self.android_mdm_page.confirm_received_alert(download_tips)
                log.info("设备点击确认下载")
                # check download record in device
                now_time = self.ota_page.get_current_time()
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                        log.info("存在： %s的下载记录" % release_info["package_name"])
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                        log.error("@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]

                log.info("检测到下载记录")
                # check the app action in ota upgrade logs, if download complete or upgrade complete, break
                self.ota_page.go_to_new_address("ota/log")

                package_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                log.info("第一次下载的的ota package size: %s" % str(package_size))
                for i in range(times):
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    log.info("***********第%d次重启************" % (i + 1))
                    try:
                        self.android_mdm_page.confirm_received_alert(download_tips)
                        log.info("设备显示下载提示并且确认下载")
                    except Exception:
                        log.error("@@@@开机恢复网络后一段时间内没有接受到下载的提示， 请检查！！！！")
                        assert "@@@@开机恢复网络后一段时间内没有接受到下载的提示， 请检查！！！！"
                    now_time = self.ota_page.get_current_time()
                    while True:
                        current_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                        log.info("重启%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                        if current_size == act_ota_package_size:
                            log.error("@@@@请检查ota 升级包大小是否适合！！！！")
                            assert False, "@@@@请检查ota 升级包大小是否适合！！！！"
                        if current_size > package_size:
                            package_size = current_size
                            break
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                            log.error("@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载")
                            assert False, "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载"
                        self.ota_page.time_sleep(1)
                log.info("*******************完成%d次重启*********************************" % (times + 1))

                now_time = self.ota_page.get_current_time()
                while True:
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
                        log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
                        log.info("下载完成后的 package_hash_value：%s" % str(package_hash_value))
                        break

                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 1200):
                        err_msg = "@@@@重启%d次， 20分钟后还没有下载完相应的ota package， 请检查！！！" % (times + 1)
                        log.error(err_msg)
                        print(err_msg)
                        assert False, err_msg
                    self.ota_page.time_sleep(10)
                log.info("***************终端下载完ota升级包*************************")
                self.ota_page.go_to_new_address("ota/log")
                report_now_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台显示的升级状态： %s" % action)
                        if self.ota_page.get_action_status(action) == 2 or self.ota_page.get_action_status(action) == 4 \
                                or self.ota_page.get_action_status(action) == 3:
                            log.info("***************下载完ota升级包*************************")
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(report_now_time, 120):
                        if self.ota_page.service_is_normal():
                            err_msg = "@@@@终端下载完升级包后， 平台3分钟还没有下载完相应的ota package， 请检查！！！"
                            log.error(err_msg)
                            print(err_msg)
                            assert False, err_msg
                        else:
                            self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                            report_now_time = self.ota_page.get_current_time()
                    self.ota_page.time_sleep(5)
                    self.ota_page.refresh_page()

                self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_alert_show()
                log.info("检测到有升级提示框")
                try:
                    self.android_mdm_page.click_cancel_btn()
                except Exception as e:
                    pass
                log.info("*******************OTA重启%d次断点续传用例结束***************************" % (times + 1))
                break
            except Exception as e:
                if self.ota_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.ota_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()
                    self.ota_page.go_to_new_address("ota")

    @allure.feature('MDM_public')
    @allure.story('MDM-Show')
    @allure.title("public case-应用满屏推送--请在附件查看满屏截图效果")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_app_full_screen(self, del_all_app_release_log, del_all_app_uninstall_release_log, go_to_app_page,
                                     uninstall_multi_apps):
        release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        while True:
            try:
                log.info("*******************应用满屏推送用例开始***************************")
                self.android_mdm_page.screen_keep_on()
                file_path = self.app_page.get_apk_path(release_info["package_name"])
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version

                # self.android_mdm_page.uninstall_app(release_info["package"])
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # check if device is online
                self.app_page.go_to_new_address("devices")
                opt_case.check_single_device(release_info["sn"])

                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % app_size)
                # check file hash value in directory Param/package
                act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"])
                log.info("act_ota_package_hash_value: %s" % act_apk_package_hash_value)
                # go to app page
                self.app_page.go_to_new_address("apps")
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info, kiosk_mode=True)

                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        log.info("存在app：%s的下载记录" % shell_app_apk_name)
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                print("**********************下载记录检测完毕*************************************")
                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原来是的 hash value: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("设备下载ota 包的下载记录: %s" % original_hash_value)
                    if original_hash_value == shell_hash_value:
                        log.info("终端检测到ota包下载完成")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        log.error("@@@@应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        assert False, "@@@@应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(5)
                log.info("**********************终端下载完成检测完毕*************************************")

                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(1)
                log.info("**********************终端安装完毕*************************************")

                self.app_page.time_sleep(5)
                self.app_page.go_to_new_address("apps/logs")
                report_now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示的升级状态： %s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            log.info("平台上报升级完成")
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_now_time, 3):
                        if self.app_page.service_is_normal():
                            log.error("@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            print("===================服务崩溃了==================================")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            print("===================服务器恢复了==================================")
                            report_now_time = self.app_page.get_current_time()

                    self.app_page.time_sleep(5)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)

                log.info("*******************静默安装完成***************************")

                self.android_mdm_page.confirm_app_is_running(release_info["package"])
                log.info("当前运行的app为： %s" % release_info["package_name"])
                base_directory = "APP_Full_Screen"
                image_before_reboot = "%s\\app_full_screen_before_reboot.jpg" % base_directory
                self.android_mdm_page.save_screenshot_to(image_before_reboot)
                self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_before_reboot,
                                                       "app_full_screen_before_reboot")
                log.info("重启设备")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("设备启动完成")
                self.android_mdm_page.confirm_app_start(release_info["package"])
                image_after_reboot = "%s\\app_full_screen_after_reboot.jpg" % base_directory
                self.android_mdm_page.confirm_app_is_running(release_info["package"])
                log.info("当前运行的app为： %s" % release_info["package_name"])
                self.android_mdm_page.save_screenshot_to(image_after_reboot)
                self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_after_reboot,
                                                       "app_full_screen_after_reboot")
                self.android_mdm_page.stop_app(release_info["package"])
                log.info("*******************应用满屏推送用例结束***************************")
                break
            except Exception as e:
                if self.app_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.app_page.go_to_new_address("apps")

    @allure.feature('MDM_public')
    @allure.title("public case-推送text.zip文件")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_release_normal_files(self, del_all_content_release_logs):
        # "All Files" "Normal Files" "Boot Animations" "Wallpaper" "LOGO"
        while True:
            try:
                log.info("*******************推送文件用例开始***************************")
                self.android_mdm_page.screen_keep_on()
                animations = test_yml["Content_info"]["normal_file"]
                release_to_path = "%s/aimdm" % self.android_mdm_page.get_internal_storage_directory()
                grep_cmd = "ls %s" % release_to_path
                # if the file is existed, delete it
                for animation in animations:
                    if animation in self.android_mdm_page.u2_send_command(grep_cmd):
                        self.android_mdm_page.rm_file("%s/%s" % (release_to_path, animation))
                    opt_case.check_single_device(self.device_sn)
                    self.content_page.go_to_new_address("content")
                    file_path = conf.project_path + "\\Param\\Content\\%s" % animation
                    file_size = self.content_page.get_file_size_in_windows(file_path)
                    log.info("获取到的文件 的size(bytes): %s" % str(file_size))
                    file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s " % animation, directory="Content")
                    log.info("文件的hash_value: %s" % str(file_hash_value))
                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(self.content_page.get_current_time()))
                    self.content_page.time_sleep(4)
                    self.content_page.search_content('Normal Files', animation)
                    release_info = {"sn": self.device_sn, "content_name": animation}
                    self.content_page.time_sleep(3)
                    assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有相关文件： %s, 请检查" % animation
                    self.content_page.release_content_file(self.device_sn, file_path=release_to_path)
                    log.info("@@@@推送文件指令下达成功")
                    now_time = self.content_page.get_current_time()
                    while True:
                        if self.android_mdm_page.download_file_is_existed(animation):
                            log.info("终端检测到文件：%s的下载记录" % animation)
                            break
                        if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                            log.error("@@@@终端检测不到到文件：%s的下载记录" % animation)
                            assert False, "@@@@终端检测不到到文件：%s的下载记录" % animation
                        self.content_page.time_sleep(5)
                    log.info("*************************************文件下载记录检测完毕**************************************")
                    now_time = self.content_page.get_current_time()
                    while True:
                        shell_file_hash_value = self.android_mdm_page.calculate_sha256_in_device(animation)
                        log.info("终端检测到文件的hash 值为： %s" % shell_file_hash_value)
                        if file_hash_value == shell_file_hash_value:
                            log.info("终端检测到文件的hash值与原来的一致")
                            break
                        if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 1200):
                            log.error("超过20分钟终端检测到文件的hash值与原来的不一致")
                            assert False, "超过20分钟终端检测到文件的hash值与原来的不一致"
                        self.content_page.time_sleep(10)
                    log.info("*************************************终端检测到文件下载完毕**************************************")
                    self.content_page.go_to_new_address("content/log")
                    report_now_time = self.content_page.get_current_time()
                    while True:
                        upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                        if len(upgrade_list) != 0:
                            action = upgrade_list[0]["Action"]
                            log.info("平台检测到upgrade log 的action: %s" % action)
                            if self.content_page.get_action_status(action) == 7:
                                log.info("平台显示文件设置完毕")
                                break
                        # wait upgrade 3 min at most
                        if self.content_page.get_current_time() > self.content_page.return_end_time(report_now_time, 180):
                            print(upgrade_list)
                            if self.content_page.service_is_normal():
                                log.error("@@@@3分钟平台还没有设置完相应的文件， 请检查！！！")
                                assert False, "@@@@3分钟平台还没有设置完相应的文件， 请检查！！！"
                            else:
                                self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                                report_now_time = self.content_page.get_current_time()
                        self.content_page.time_sleep(3)
                        self.content_page.refresh_page()
                    self.content_page.time_sleep(5)
                    assert animation in self.android_mdm_page.u2_send_command(
                        grep_cmd), "@@@@文件没有释放到设备指定的路径%s, 请检查！！！" % release_to_path
                    log.info("终端检测到文件已经推送到指定的路径： %s" % release_to_path)
                log.info("*******************推送文件用例结束***************************")
                break
            except Exception as e:
                if self.content_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.app_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.delete_all_content_release_log()
                    self.android_mdm_page.del_all_content_file()
                    self.android_mdm_page.screen_keep_on()

    @allure.feature('MDM_public')
    @allure.title("public case-多应用推送")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_release_multi_apps(self, del_all_app_release_log, del_download_apk, uninstall_multi_apps):
        while True:
            try:
                log.info("*******************多应用推送用例开始***************************")
                release_info = {"sn": self.device_sn, "silent": "Yes", "download_network": "NO Limit", "version": False}
                apks = [test_yml["app_info"][apk_name] for apk_name in test_yml["app_info"] if
                        apk_name not in ["high_version_app", "low_version_app"]]
                apks = list(set(apks))
                log.info("推送到的应用： %s" % ",".join(apks))
                self.app_page.go_to_new_address("apps/releases")
                self.app_page.delete_all_app_release_log()
                # self.android_mdm_page.uninstall_multi_apps()

                apks_packages = [self.android_mdm_page.get_apk_package_name(self.android_mdm_page.get_apk_path(apk)) for apk in
                                 apks]
                apks_versions = [self.android_mdm_page.get_apk_package_version(self.android_mdm_page.get_apk_path(apk)) for apk
                                 in apks]

                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("设备重启成功")
                self.app_page.refresh_page()

                # check if device is online
                self.app_page.go_to_new_address("devices")
                opt_case.check_single_device(release_info["sn"])
                log.info("检测到设备：%s 在线" % release_info["sn"])
                # go to app page and release multi apps one by one
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                flag = -1
                for release_app in apks:
                    flag += 1
                    self.app_page.go_to_new_address("apps")
                    self.app_page.search_app_by_name(release_app)
                    app_list = self.app_page.get_apps_text_list()
                    if len(app_list) == 0:
                        assert False, "@@@@检测到平台没有 %s, 请检查！！！" % release_app
                    self.app_page.click_release_app_btn()
                    self.app_page.input_release_app_info(release_info)

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
                                log.info("检测到apk：%s 的下载记录" % shell_app_apk_name)
                    if len(downloading_apks) == len(apks_packages):
                        log.info("检测到全部的apk都有下载记录")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        diff_list = [package for package in apks_packages if package not in downloading_apks]
                        download_record = ",".join(diff_list)
                        log.info("@@@@多应用推送中超过30分钟还没有%s的下载记录" % download_record)
                        assert False, "@@@@多应用推送中超过30分钟还没有%s的下载记录" % download_record
                log.info("**********************下载记录检测完毕*************************************")
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
                        log.error("@@@@多应用推送中超过30分钟还没有完成%s的下载" % download_missing_record)
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
                        log.info("所有的app全部安装完毕")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        diff_list = [package for package in apks_packages if package not in installed_apks]
                        uninstalled_record = ",".join(diff_list)
                        log.info("@@@@多应用推送下载完成后超过3分钟还没有%s的安装记录" % uninstalled_record)
                        assert False, "@@@@多应用推送下载完成后超过3分钟还没有%s的安装记录" % uninstalled_record
                log.info("******************************设备检测到所有的app安装记录检测完毕****************************************")

                # check if all installed success logs in app upgrade logs
                self.app_page.go_to_new_address("apps/logs")
                report_installed = []
                report_time = self.app_page.get_current_time()
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
                                log.info("平台显示apk: %s的upgrade action为： %s" % (installed_app, action))
                                if self.app_page.get_action_status(action) == 4:
                                    report_installed.append(installed_app)
                            # if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                            #     assert False, "@@@@设备已经安装完相应的app， 请检查！！！"
                            self.app_page.time_sleep(3)
                            self.app_page.refresh_page()
                    if len(report_installed) == len(apks_packages):
                        log.info("已经全部安装完所有的app")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_time, 300):
                        diff_list = [package for package in apks_packages if package not in report_installed]
                        uninstalled_report = ",".join(diff_list)
                        if self.app_page.service_is_normal():
                            log.error("@@@@多应用推送中设备已经安装完毕所有的app, 平台超过5分钟还上报%s的安装记录" % uninstalled_report)
                            assert False, "@@@@多应用推送中设备已经安装完毕所有的app, 平台超过5分钟还上报%s的安装记录" % uninstalled_report
                        else:
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            report_time = self.app_page.get_current_time()
                log.info("*******************多应用推送用例结束***************************")
                break
            except Exception as e:
                if self.app_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.app_page.recovery_after_service_unavailable("apps", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.app_page.go_to_new_address("apps")

    @allure.feature('MDM_public')
    @allure.story('MDM-Show')
    @allure.title("public case-静默卸载正在运行中的app： 静默卸载/卸载正在运行的app")
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_silent_uninstall_app(self, del_all_app_release_log, del_all_app_uninstall_release_log, uninstall_multi_apps,
                           go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes"}
        while True:
            try:
                log.info("*******************静默卸载正在运行中的app 用例开始***************************")
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                # install app for uninstall
                self.android_mdm_page.confirm_app_installed(file_path)
                # check if device is online
                self.app_page.go_to_new_address("devices")
                opt_case.check_single_device(release_info["sn"])
                log.info("检测到设备在线")
                # go to app release page
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])

                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@检测到平台没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@检测到平台没有 %s, 请检查！！！" % release_info["package_name"]

                # start app and then uninstall it， added recently
                # self.android_mdm_page.start_app(release_info["package"])
                self.android_mdm_page.confirm_app_is_running(release_info["package"])
                self.android_mdm_page.screen_keep_on()
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                # self.android_mdm_page
                self.app_page.click_uninstall_app_btn()
                self.app_page.input_uninstall_app_info(release_info)
                log.info("筋膜卸载指令下达成功")

                self.app_page.go_to_new_address("apps/uninstalllogs")
                report_time = self.app_page.get_current_time()
                while True:
                    upgrade_log = self.app_page.get_app_latest_uninstall_log(send_time, release_info)
                    if len(upgrade_log) != 0:
                        action = upgrade_log[0]["Action"]
                        log.info("平台状态显示upgrade action: %s" % action)
                        if self.app_page.get_action_status(action) == 0:
                            log.info("平台显示完成app的静默卸载")
                            assert not self.android_mdm_page.app_is_installed(
                                release_info["package"]), "@@@@平台显示已经卸载app：%s, 检测到设备还没卸载， 请检查！！！" % release_info[
                                "package_name"]
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_time, 180):
                        if self.app_page.service_is_normal():
                            log.error("@@@@3分钟还没有卸载完相应的app， 请检查！！！")
                            assert False, "@@@@3分钟还没有卸载完相应的app， 请检查！！！"
                        else:
                            self.app_page.recovery_after_service_unavailable("apps/uninstalllogs", case_pack.user_info)
                            report_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(3)
                    self.app_page.refresh_page()
                log.info("****************************************静默卸载完成**********************************")
                break
            except Exception as e:
                if self.app_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
                    self.app_page.go_to_new_address("apps")

    @allure.feature('MDM_public-test')
    @allure.title("public case- 静默ota升级")
    # @pytest.mark.flaky(reruns=2, reruns_delay=1)
    def test_silent_ota_upgrade(self, del_all_ota_release_log, go_to_ota_page, delete_ota_package_relate):
        while True:
            try:
                log.info("*******************静默ota升级用例开始***************************")
                release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                                "silent": 0, "category": "NO Limit", "network": "NO Limit"}
                download_tips = "Foundanewfirmware,whethertoupgrade?"
                upgrade_tips = "whethertoupgradenow?"
                self.android_mdm_page.del_updated_zip()
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                try:
                    assert self.ota_page.transfer_version_into_int(
                        current_firmware_version) < self.ota_page.transfer_version_into_int(
                        release_info["version"]), \
                        "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                except AttributeError as e:
                    log.info("*******************静默ota升级用例结束***************************")
                    if self.silent_ota_upgrade_flag == 1:
                        assert True
                    else:
                        assert False, e

                # reboot
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("成功重启设备")
                # search package
                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("设备当前固件版本：%s" % device_current_firmware_version)
                log.info("目标固件版本为 %s :" % release_info["version"])
                ota_package_size = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
                log.info("原始文件的hash值 ota_package_hash_value： %s" % str(act_ota_package_hash_value))
                act_ota_package_size = self.ota_page.get_zip_size(ota_package_size)
                log.info("原始文件的大小（bytes）： %s" % str(act_ota_package_size))
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.ota_page.get_current_time()))
                print("send_time", send_time)
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                self.ota_page.input_release_OTA_package(release_info, is_silent=True)
                log.info("推送ota package 指令下达成功")
                # check download record in device
                now_time = self.ota_page.get_current_time()
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                        log.info("终端检测到 %s 的下载记录" % release_info["package_name"])
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                        log.error("@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]
                    self.ota_page.time_sleep(10)

                self.ota_page.go_to_new_address("ota/log")
                upgrade_flag = 0
                download_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台upgrade log action: %s" % action)
                        if self.ota_page.get_action_status(action) in [2, 3, 4]:
                            log.info("*****************平台upgrade log显示ota安装包下载完成*****************")
                            if action == 4:
                                log.info("*****************平台upgrade log显示ota升级成功*****************")
                                upgrade_flag = 1
                            break
                    # wait upgrade 3 min at most
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(download_time, 600):
                        self.silent_ota_upgrade_flag = 1
                        if self.ota_page.service_is_normal():
                            log.error("@@@@30分钟还没有下载完相应的固件， 请检查！！！")
                            assert False, "@@@@30分钟还没有下载完相应的固件， 请检查！！！"
                        else:
                            self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                            download_time = self.app_page.get_current_time()
                    self.ota_page.time_sleep(30)
                    self.ota_page.refresh_page()

                if upgrade_flag == 0:
                    self.ota_page.refresh_page()
                    report_time = self.ota_page.get_current_time()
                    while True:
                        info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                        if len(info) != 0:
                            action = info[0]["Action"]
                            log.info("平台upgrade log action: %s" % action)
                            if self.ota_page.get_action_status(action) == 4:
                                log.info("*****************平台upgrade log显示ota升级成功*****************")
                                break
                        # wait upgrade 3 min at most
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(report_time, 600):
                            if self.ota_page.service_is_normal():
                                self.silent_ota_upgrade_flag = 1
                                log.error("@@@@30分钟还没有升级相应的ota包， 请检查！！！")
                                assert False, "@@@@30分钟还没有升级相应的ota包， 请检查！！！"
                            else:
                                self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                                report_time = self.ota_page.get_current_time()
                        self.ota_page.time_sleep(30)
                        self.ota_page.refresh_page()
                log.info("************************平台显示ota安装升级完成完成*************************************")
                self.android_mdm_page.time_sleep(5)
                self.android_mdm_page.device_boot(self.wifi_ip)
                log.info("设备启动成功")
                after_upgrade_version = self.android_mdm_page.check_firmware_version()
                log.info("设备升级后的固件版本：%s" % after_upgrade_version)
                # assert self.ota_page.transfer_version_into_int(
                #     device_current_firmware_version) != self.ota_page.transfer_version_into_int(after_upgrade_version), \
                #     "@@@@ota升级失败， 还是原来的版本%s！！" % device_current_firmware_version
                # assert self.ota_page.transfer_version_into_int(release_info["version"]) == \
                #        self.ota_page.transfer_version_into_int(
                #            after_upgrade_version), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
                assert self.ota_page.remove_space(str(after_upgrade_version)) == self.ota_page.remove_space(release_info["version"]), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
                log.info("*******************静默ota升级用例结束***************************")
                break
            except Exception as e:
                if self.ota_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.content_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.ota_page.go_to_new_address("ota")
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()

    @allure.feature('MDM_public')
    @allure.title("public case- 静默升级系统app/推送安装成功后自动运行app")
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_upgrade_system_app(self, del_all_app_release_log, del_download_apk, uninstall_system_app):
        while True:
            try:
                log.info("*******************静默升级系统app用例开始/推送安装成功后自动运行app***************************")
                release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                                "silent": "Yes", "download_network": "NO Limit", "auto_open": "YES"}
                file_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                #
                # # install low version system application
                # # set app as system app
                self.android_mdm_page.wifi_adb_root(self.wifi_ip)
                # assert not self.android_mdm_page.app_is_installed(
                #     self.android_mdm_page.get_apk_package_name(file_path))
                # push file to system/app
                now_time = self.android_mdm_page.get_current_time()
                while True:
                    self.android_mdm_page.push_file_to_device(
                        self.android_mdm_page.get_apk_path(test_yml['app_info']['low_version_app']), "/system/app/")
                    if test_yml['app_info']['low_version_app'] in self.android_mdm_page.u2_send_command(
                            "ls /system/app"):
                        log.info(
                            "成功推送文件%s 到终端：%s, 标志为系统app" % (test_yml['app_info']['low_version_app'], "/system/app/"))
                        log.info(self.android_mdm_page.u2_send_command("ls /system/app"))
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("无法推送文件%s 到终端：%s" % (test_yml['app_info']['low_version_app'], "/system/app/"))
                        assert False, "无法推送文件%s 到终端：%s" % (test_yml['app_info']['low_version_app'], "/system/app/")
                    self.android_mdm_page.time_sleep(2)
                # print(self.android_mdm_page.u2_send_command("ls /system/app"))

                self.android_mdm_page.reboot_device_root(self.wifi_ip)
                log.info("重启")
                assert self.android_mdm_page.app_is_installed(
                    self.android_mdm_page.get_apk_package_name(file_path)), "@@@没有安装系统应用， 请检查！！！！"
                log.info("已经安装好了系统应用： %s" % self.android_mdm_page.get_apk_package_name(file_path))
                # release high version system app
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version
                # check if device is online
                self.app_page.go_to_new_address("devices")
                opt_case.check_single_device(release_info["sn"])
                log.info("检测到设备 %s 在线" % release_info["sn"])
                # app_size_mdm = self.page.get_app_size()  for web
                # check app size(bytes) in windows
                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % str(app_size))

                # go to app page
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@平台没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@平台没有 %s, 请检查！！！" % release_info["package_name"]
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.click_release_app_btn()
                try:
                    self.app_page.input_release_app_info(release_info)
                    log.info("app推送指令下达成功")
                except Exception as e:
                    pass
                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        log.info("终端检测到 %s的 下载记录" % shell_app_apk_name)
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************下载记录检测完毕*************************************")

                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原始app的 hash 值： %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("shell_hash_value: %s" % original_hash_value)
                    if original_hash_value == shell_hash_value:
                        log.info("检测到原始文件和终端下载后的文件内容一致性， 下载完成")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        log.error("@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(60)
                log.info("**********************下载完成检测完毕*************************************")
                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.app_page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        log.info("目标版本为：%s" ".".join(str(version_installed)))
                        current_version = self.app_page.transfer_version_into_int(release_info["version"])
                        log.info("当前版本为： %s" % ".".join(str(current_version)))
                        if version_installed == current_version:
                            log.info("系统app静默覆盖安装完成")
                            break
                        else:
                            log.error("@@@@覆盖安装后版本与木目标版本不一致， 请检查！！！！")
                            assert False, "@@@@覆盖安装后版本与木目标版本不一致， 请检查！！！！"
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(5)
                self.app_page.time_sleep(5)
                log.info("**********************终端成功静默安装系统app*************************************")

                self.app_page.go_to_new_address("apps/logs")
                self.app_page.refresh_page()
                report_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示的upgrade action为： %s" % action)
                        break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_time, 300):
                        if self.app_page.service_is_normal():
                            log.error("@@@@5分钟平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            report_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(5)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)
                log.info("************************推送安装成功后自动运行app*****************************")
                try:
                    self.android_mdm_page.confirm_app_auto_running(release_info["package"], 120)
                except AttributeError:
                    log.error("app 推送选择了安装完成后自动运行app, app安装完后2分钟内还没自动运行")
                try:
                    self.android_mdm_page.stop_app(release_info["package"])
                    self.android_mdm_page.rm_file("system/app/%s" % test_yml['app_info']['low_version_app'])
                except Exception as e:
                    pass
                log.info("************************推送安装成功后自动运行app成功*****************************")
                log.info("***************静默升级系统app/推送安装成功后自动运行app用例结束*********************")
                break
            except Exception as e:
                if self.app_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.confirm_system_app_uninstalled()
                    self.app_page.go_to_new_address("apps")

    @allure.feature('MDM_public')
    @allure.title("public case-推送开机logo/动画")
    @allure.story('MDM-Show')
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_release_boot_logo_and_animation(self, del_all_content_release_logs, del_all_content_file):
        # "All Files" "Normal Files" "Boot Animations" "Wallpaper" "LOGO"
        while True:
            try:
                log.info("*******************推送开机logo/动画开始***************************")
                self.android_mdm_page.screen_keep_on()
                logos = test_yml["Content_info"]["boot_logo"]
                animation = test_yml["Content_info"]["boot_animation"][0]

                opt_case.check_single_device(self.device_sn)
                self.content_page.go_to_new_address("content")
                file_path = conf.project_path + "\\Param\\Content\\%s" % animation
                file_size = self.content_page.get_file_size_in_windows(file_path)
                log.info("获取到的文件 的size(bytes): %s" % str(file_size))
                file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % animation, directory="Content")
                log.info("file_hash_value: %s" % str(file_hash_value))
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.content_page.get_current_time()))
                self.content_page.time_sleep(15)
                self.content_page.search_content('Boot Animations', animation)
                release_info = {"sn": self.device_sn, "content_name": animation}
                self.content_page.time_sleep(3)
                assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有机动画： %s, 请检查" % animation
                self.content_page.release_content_file(self.device_sn)
                log.info("动画压缩包 ：%s 推送成功" % animation)
                now_time = self.content_page.get_current_time()
                while True:
                    if self.android_mdm_page.download_file_is_existed(animation):
                        break
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                        log.error("@@@@没有%s下载记录， 请检查！！！" % animation)
                        assert False, "@@@@没有%s下载记录， 请检查！！！" % animation
                    self.content_page.time_sleep(5)
                log.info("****************检测到终端有 %s 的下载记录********************" % animation)
                now_time = self.content_page.get_current_time()
                while True:
                    if file_hash_value == self.android_mdm_page.calculate_sha256_in_device(animation):
                        break
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 900):
                        log.error("@@@@超过15分钟还没有下载完毕，请检查！！！")
                        assert False, "@@@@超过15分钟还没有下载完毕，请检查！！！"
                    self.content_page.time_sleep(5)

                log.info("********************设备检测到文件:%s下载完毕***********************" % animation)
                # check upgrade
                self.content_page.go_to_new_address("content/log")
                report_now_time = self.content_page.get_current_time()
                while True:
                    upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台upgrade action为： %s" % action)
                        if self.content_page.get_action_status(action) == 7:
                            break
                    # wait upgrade 3 min at most
                    if self.content_page.get_current_time() > self.content_page.return_end_time(report_now_time, 180):
                        if self.content_page.service_is_normal():
                            log.info("@@@@3分钟还没有设置完相应的开机动画， 请检查！！！")
                            assert False, "@@@@3分钟还没有设置完相应的开机动画， 请检查！！！"
                        else:
                            self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                            report_now_time = self.content_page.get_current_time()
                    self.content_page.time_sleep(5)
                    self.content_page.refresh_page()
                log.info("***********************动画推送完成***************************")
                # release logo
                i = 0
                for logo in logos:
                    i += 1
                    opt_case.check_single_device(self.device_sn)
                    self.content_page.go_to_new_address("content")
                    file_path = conf.project_path + "\\Param\\Content\\%s" % logo
                    file_size_logo = self.content_page.get_file_size_in_windows(file_path)
                    log.info("获取到的文件 的size(bytes): %s" % str(file_size_logo))
                    file_hash_value_logo = self.content_page.calculate_sha256_in_windows(logo, directory="Content")
                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(self.content_page.get_current_time()))
                    self.content_page.time_sleep(10)
                    self.content_page.search_content('LOGO', logo)
                    release_info = {"sn": self.device_sn, "content_name": logo}
                    self.content_page.time_sleep(3)
                    assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有该logo图片： %s, 请检查" % logo
                    self.content_page.release_content_file(self.device_sn)

                    # check upgrade
                    now_time = self.content_page.get_current_time()
                    while True:
                        if self.android_mdm_page.download_file_is_existed(logo):
                            break
                        if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                            log.error("@@@@没有相应的下载记录， 请检查！！！")
                            assert False, "@@@@没有相应的下载记录， 请检查！！！"
                        self.content_page.time_sleep(5)
                    log.info("*************************************文件下载记录检测完毕**************************************")
                    now_time = self.content_page.get_current_time()
                    while True:
                        if file_size_logo == self.android_mdm_page.get_file_size_in_device(logo):
                            log.info("开机logo的大小为： %s" % str(file_size_logo))
                            log.info("开机logo的hash值为： %s" % str(self.android_mdm_page.calculate_sha256_in_device(logo)))
                            assert file_hash_value_logo == self.android_mdm_page.calculate_sha256_in_device(logo), "@@@@文件大小一样， hash256值不一致请检查！！"
                            break
                        if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 200):
                            log.error("@@@@超过15分钟还没有下载完毕，请检查！！！")
                            assert False, "@@@@超过15分钟还没有下载完毕，请检查！！！"
                        self.content_page.time_sleep(5)
                    log.info("*************************************文件下载完毕**************************************")
                    self.content_page.go_to_new_address("content/log")
                    report_time = self.content_page.get_current_time()
                    while True:
                        upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                        if len(upgrade_list) != 0:
                            action = upgrade_list[0]["Action"]
                            log.info("平台 upgrade action: %s" % action)
                            if self.content_page.get_action_status(action) == 7:
                                break
                        # wait upgrade 3 min at most
                        if self.content_page.get_current_time() > self.content_page.return_end_time(report_time, 180):
                            if self.content_page.service_is_normal():
                                log.error("@@@@3分钟还没有设置完相应的开机logo， 请检查！！！")
                                assert False, "@@@@3分钟还没有设置完相应的开机logo， 请检查！！！"
                            else:
                                self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                                report_time = self.content_page.get_current_time()
                        self.content_page.time_sleep(5)
                        self.content_page.refresh_page()

                    # case_pack.AlertData().getAlert("请关掉提示框并且查看启动logo和动画")
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.content_page.time_sleep(5)

                print("*******************推送开机logo/动画结束***************************")
                log.info("*******************推送开机logo/动画结束***************************")
                break
            except Exception as e:
                if self.device_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.delete_all_content_release_log()
                    self.android_mdm_page.del_all_content_file()
                    self.android_mdm_page.screen_keep_on()

    @allure.feature('MDM_public')
    @allure.title("public case-无线休眠推送app")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_report_device_sleep_status(self, del_app_install_uninstall_release_log, go_to_device_page, uninstall_multi_apps):
        while True:
            try:
                log.info("*******************无线休眠推送app用例开始***************************")
                for i in range(1):
                    log.info("******************%d**********************" % (i + 1))
                    self.android_mdm_page.close_mobile_data()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.android_mdm_page.screen_keep_on()
                    self.android_mdm_page.back_to_home()
                    # self.android_mdm_page.confirm_unplug_usb_wire()
                    # case_pack.AlertData().getAlert("请拔开USB线再点击确定")
                    opt_case.check_single_device(self.device_sn)
                    usb_serial.confirm_relay_opened()
                    log.info("打开继电器")
                    release_info = {"package_name": test_yml['app_info']['other_app'], "sn": self.device_sn,
                                    "silent": "Yes", "download_network": "NO Limit"}
                    self.app_page.go_to_new_address("apps")
                    app_list = self.app_page.get_apps_text_list()
                    if len(app_list) == 0:
                        assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                    file_path = self.app_page.get_apk_path(release_info["package_name"])
                    package = self.app_page.get_apk_package_name(file_path)
                    release_info["package"] = package
                    version = self.app_page.get_apk_package_version(file_path)
                    release_info["version"] = version

                    app_size = self.app_page.get_file_size_in_windows(file_path)
                    log.info("获取到的app 的size(bytes): %s" % str(app_size))
                    # check file hash value in directory Param/package
                    act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(release_info["package_name"])
                    log.info("act_ota_package_hash_value: %s" % str(act_apk_package_hash_value))
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
                    log.info("设备清屏成功")
                    self.device_page.select_device(self.device_sn)
                    self.device_page.send_message(msg)
                    log.info("发送消息")
                    if not self.android_mdm_page.public_alert_show(120):
                        log.error("@@@@平台显示设备在线， 发送消息2分钟后还没收到消息")
                        assert False, "@@@@平台显示设备在线， 发送消息2分钟后还没收到消息"
                    self.android_mdm_page.confirm_received_text(msg, timeout=5)
                    log.info('设备接收到消息')
                    try:
                        self.android_mdm_page.click_msg_confirm_btn()
                        self.android_mdm_page.confirm_msg_alert_fade(msg)
                    except Exception:
                        pass
                    usb_serial.confirm_relay_closed()
                    log.info("下电")
                    self.android_mdm_page.device_sleep()
                    log.info("设备灭屏")
                    # self.android_mdm_page.time_sleep(test_yml["android_device_info"]["sleep_time"])
                    self.android_mdm_page.confirm_device_no_existed(self.wifi_ip)
                    log.info("设备已经不在线，确认设备已经进入深度休眠模式")
                    self.android_mdm_page.time_sleep(600)
                    log.info("设备休眠结束")
                    # wakeup device
                    usb_serial.confirm_relay_opened()
                    log.info("上电")
                    # check if the device is existed
                    self.android_mdm_page.device_existed(test_yml["android_device_info"]["device_name"])
                    try:
                        self.android_mdm_page.ping_network(300)
                    except AttributeError:
                        assert False, "休眠唤醒后wifi无法上网"
                    log.info("wifi环境下可以上网")
                    self.android_mdm_page.device_is_existed(self.wifi_ip)
                    log.info("检测到设备在线， 成功唤醒设备")
                    self.android_mdm_page.screen_keep_on()
                    self.device_page.refresh_page()
                    opt_case.check_single_device(self.device_sn)
                    log.info("检测到设备在线")
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
                    self.app_page.time_sleep(10)
                    self.app_page.search_app_by_name(release_info["package_name"])
                    self.app_page.click_release_app_btn()
                    self.app_page.input_release_app_info(release_info)
                    log.info("推送app指令下达")
                    # check app download record in device
                    now_time = self.app_page.get_current_time()
                    shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                    log.info("app在终端显示的命名为：%s" % shell_app_apk_name)
                    while True:
                        if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                            log.info("终端download文件夹下面存在app：%s的下载记录" % shell_app_apk_name)
                            break
                        if self.app_page.get_current_time() > self.app_page.return_end_time(now_time):
                            log.error("终端download文件夹下面不存在app：%s的下载记录" % shell_app_apk_name)
                            assert False, "终端download文件夹下面不存在app：%s的下载记录" % shell_app_apk_name
                        self.app_page.time_sleep(3)

                    # check if the upgrade log appeared, if appeared, break
                    self.app_page.go_to_new_address("apps/logs")

                    # check the app action in app upgrade logs, if download complete or upgrade complete, break
                    report_time = self.app_page.get_current_time()
                    while True:
                        upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                        if len(upgrade_list) != 0:
                            action = upgrade_list[0]["Action"]
                            log.info("平台显示的状态： %s" % action)
                            if self.app_page.get_action_status(action) == 2 or self.app_page.get_action_status(action) == 4 \
                                    or self.app_page.get_action_status(action) == 3:
                                # check the app size in device, check if app download fully
                                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                                size = self.android_mdm_page.get_file_size_in_device(shell_app_apk_name)
                                log.info("终端下载后的的size大小： %s" % str(size))
                                package_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                                log.info("原来升级包的 package_hash_value：%s" % act_apk_package_hash_value)
                                log.info("下载完成后的 package_hash_value：%s" % package_hash_value)
                                assert app_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                                assert package_hash_value == act_apk_package_hash_value, "@@@@平台显示下载完成，终端的apk和原始的apkSHA-256值不一致， 请检查！！！！"
                                break
                        # wait 20 mins
                        if self.app_page.get_current_time() > self.app_page.return_end_time(report_time, 300):
                            if self.app_page.service_is_normal():
                                log.error("@@@@30分钟还没有下载完相应的app， 请检查！！！")
                                assert False, "@@@@30分钟还没有下载完相应的app， 请检查！！！"
                            else:
                                self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                                log.info("服务器503恢复后继续执行")
                                report_time = self.app_page.get_current_time()
                        self.app_page.time_sleep(10)
                        self.app_page.refresh_page()
                    log.info("安装包下载完成")
                    # check upgrade
                    report_upgrade_time = self.app_page.get_current_time()
                    while True:
                        upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                        if len(upgrade_list) != 0:
                            action = upgrade_list[0]["Action"]
                            log.info("平台显示的状态： %s" % action)
                            if self.app_page.get_action_status(action) == 4:
                                if self.android_mdm_page.app_is_installed(release_info["package"]):
                                    log.info("检测到设备已经安装了app: %s" % release_info["package"])
                                    break
                                else:
                                    log.error("@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！")
                                    assert False, "@@@@平台显示已经完成安装了app, 终端发现没有安装此app， 请检查！！！！"
                        # wait upgrade 3 min at most
                        if self.app_page.get_current_time() > self.app_page.return_end_time(report_upgrade_time, 180):
                            if self.app_page.service_is_normal():
                                log.error("@@@@3分钟还没有安装完相应的app， 请检查！！！")
                                assert False, "@@@@3分钟还没有安装完相应的app， 请检查！！！"
                            else:
                                self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                                log.info("服务器503后恢复")
                                report_upgrade_time = self.app_page.get_current_time()
                        self.app_page.time_sleep(5)
                        self.app_page.refresh_page()
                    self.app_page.delete_app_install_and_uninstall_logs()
                break
            except Exception as e:
                if self.device_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
                    self.device_page.go_to_new_address("devices")

    @allure.feature('MDM_public111')
    @allure.title("Devices- 关机 -- test in the last")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_device_shutdown(self):
        while True:
            try:
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
                now_time = self.device_page.get_current_time()
                while True:
                    if "Off" in opt_case.get_single_device_list(sn)[0]["Status"]:
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(now_time, 60):
                        assert False, "@@@@已发送关机命令， 设备还显示在线状态"
                    self.device_page.refresh_page()
                break
            except Exception as e:
                if self.device_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.device_page.go_to_new_address("devices")

