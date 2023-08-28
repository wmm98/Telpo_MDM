import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()

data_cate_mode = [{"cate": "台式2", "model": "M1"},
                  {"cate": "壁挂式-test", "model": "TPS980P-test"}]

devices = [{"name": "TPS980-cc", "SN": "3180980P12300283", "cate": "壁挂式", "model": "TPS980P"},
           {"name": "M1K-MM", "SN": "00002002000000000", "cate": "手持终端", "model": "M1"}]


class TestDevicesPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.DevicesPage(self.driver, 40)
        self.meg_page = case_pack.MessagePage(self.driver, 40)
        self.telpo_mdm_page = case_pack.TelpoMDMPage(self.driver, 40)

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("Devices main Page")  # 设置case的名字
    # @pytest.mark.dependency(depends=["test_TelpoMdM_Page"], scope='package')
    def test_go_to_devices_page(self):
        exp_main_title = "Total Devices"
        try:
            self.page.click_devices_btn()
            # click devices list btn  -- just for test version
            self.page.click_devices_list_btn()
            # wait Page load complete
            self.page.page_load_complete()
            # check current Page
            act_main_title = self.page.get_loc_main_title()
            now_time = self.page.get_current_time()
            while True:
                if exp_main_title in act_main_title:
                    break
                else:
                    self.page.go_to_new_address("devices")
                if self.page.get_current_time() > self.page.return_end_time(now_time):
                    log.error("@@@打开device页超时")
                    assert False, "@@@打开device页超时"
                self.page.time_sleep(1)
            log.info("当前默认的副标题为：%s" % act_main_title)
        except Exception as e:
            log.error(str(e))
            assert False

    @allure.feature('MDM_test02')
    @allure.title("Devices-add category and  model")  # 设置case的名字
    @pytest.mark.parametrize('cate_model', data_cate_mode)
    def test_add_category_model(self, cate_model):
        exp_existed_name = "name already existed"
        exp_add_cate_success = "Add Category Success"
        exp_add_mode_success = "Add Model Success"
        if not self.page.category_is_existed(cate_model["cate"]):
            self.page.click_category()
            self.page.add_category(cate_model["cate"])
            now_time = self.page.get_current_time()
            while True:
                self.page.time_sleep(1)
                if cate_model["cate"] in self.page.get_categories_list():
                    break
                if self.page.get_current_time() > self.page.return_end_time(now_time, timeout=5):
                    e = "@@@添加种类失败，请检查！！！"
                    log.error(e)
                    assert False, e

        if cate_model["model"] not in self.page.get_models_list():
            self.page.click_model()
            self.page.add_model(cate_model["model"])
            now_time = self.page.get_current_time()
            while True:
                self.page.time_sleep(1)
                if cate_model["model"] in self.page.get_models_list():
                    break
                if self.page.get_current_time() > self.page.return_end_time(now_time, timeout=5):
                    e = "@@@添加种类失败，请检查！！！"
                    log.error(e)
                    assert False, e
        self.page.confirm_add_category_box_fade()

        self.page.find_category()
        self.page.find_model()

    @allure.feature('MDM_test02')
    @allure.title("Devices-new devices")  # 设置case的名字
    @pytest.mark.parametrize('devices_list', devices)
    def test_new_devices(self, devices_list):
        exp_success_text = "Device created successfully,pls reboot device to active!"
        exp_existed_text = "sn already existed"
        try:
            # check if device is existed before test, if not, skip
            devices_sn = [device["SN"] for device in self.page.get_dev_info_list()]
            print(devices_sn)
            if devices_list["SN"] not in devices_sn:
                # check if device model is existed, if not, add model
                if devices_list["model"] not in self.page.get_models_list():
                    self.page.click_model()
                    self.page.add_model(devices_list["model"])
                    self.page.refresh_page()
                    assert devices_list["model"] in self.page.get_models_list(), "@@@model 不存在， 请检查！！！！"
                # check if device category is existed, if not, add category
                if not self.page.category_is_existed(devices_list["cate"]):
                    self.page.click_category()
                    self.page.add_category(devices_list["cate"])
                    assert self.page.category_is_existed(devices_list["cate"]), "@@@category 不存在， 请检查！！！！"

                info_len_pre = self.page.get_dev_info_length()
                print(info_len_pre)
                self.page.click_new_btn()
                self.page.add_devices_info(devices_list)
                # text = self.Page.get_alert_text()
                # print(text)
                self.page.get_add_dev_warning_alert()
                # refresh current Page and clear warning war
                self.page.refresh_page()
                info_len_pos = self.page.get_dev_info_length()
                print(info_len_pos)
                assert info_len_pre == info_len_pos - 1
                # print all devices info
                print(self.page.get_dev_info_list())
        except Exception as e:
            print("发生的异常是", e)
            assert False

    @allure.feature('MDM_test02')
    @allure.title("Devices- test check box")  # 设置case的名字
    @pytest.mark.parametrize('devices_list', devices)
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_check_boxes(self, devices_list):
        # check all btn; select all devices
        self.page.refresh_page()
        se_all_btn = self.page.select_all_devices()
        self.page.check_ele_is_selected(se_all_btn)
        se_none_btn = self.page.select_all_devices()
        self.page.check_ele_is_not_selected(se_none_btn)
        self.page.time_sleep(3)

        # select single device
        devices_info = self.page.get_dev_info_list()
        try:
            for dev_info in devices_info:
                if devices_list["SN"] in dev_info['SN']:
                    ele = self.page.select_device(devices_list["SN"])
                    # 选中
                    self.page.check_ele_is_selected(ele)
                    self.page.time_sleep(2)
                    ele_not = self.page.select_device(devices_list["SN"])
                    self.page.check_ele_is_not_selected(ele_not)
                    self.page.time_sleep(2)
        except Exception:
            assert False, "@@@元素没有没选中, 请检查！！！"

    @allure.feature('MDM_test02')
    @allure.title("Devices- test import btn")
    def test_import_devices(self):
        exp_success_text = "Add Device Success"
        # devices_info = {"cate": "手持终端", "model": "TPS980P"}
        file_path = conf.project_path + "\\Param\\device import.xlsx"
        devices_info = excel.get_template_data(file_path, "cate_model")[0]

        if devices_info["model"] not in self.page.get_models_list():
            self.page.click_model()
            self.page.add_model(devices_info["model"])
            self.page.refresh_page()
            assert devices_info["model"] in self.page.get_models_list(), "@@@model 不存在， 请检查！！！！"
        # check if device category is existed, if not, add category
        if not self.page.category_is_existed(devices_info["cate"]):
            self.page.click_category()
            self.page.add_category(devices_info["cate"])
            assert self.page.category_is_existed(devices_info["cate"]), "@@@category 不存在， 请检查！！！！"

        # click import-btn
        self.page.click_import_btn()
        self.page.import_devices_info(devices_info)
        # print(self.Page.get_alert_text())
        # if exp_success_text in self.Page.get_alert_text():
        #     self.Page.alert_fade()

        # need to add check length of data list

    @allure.feature('MDM_test02')
    @allure.title("Devices- AIMDM send message")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_send_message_to_single_device(self):
        exp_success_send_text = "Message Sent"
        # sn would change after debug with devices
        sn = "A250900P03100019"
        date_time = '%Y-%m-%d %H:%M:%S'
        self.page.refresh_page()
        now = case_pack.time.strftime(date_time, case_pack.time.localtime(case_pack.time.time()))
        msg = "%s: 12345#$**&&&&" % now
        # confirm if device is online and execute next step, if not, end the case execution
        opt_case.check_single_device(sn)

        self.page.select_device(sn)
        self.page.click_send_btn()
        self.page.msg_input_and_send(msg)
        # check alert text
        # opt_case.check_alert_text(exp_success_send_text)

        # check devices

    @allure.feature('MDM_test02')
    @allure.title("Devices- lock and unlock single device")
    def test_lock_and_unlock_single_device(self):
        # case is stable
        sn = "A250900P03100019"
        exp_lock_msg = "Device %s Locked" % sn
        exp_unlock_msg = "Device %s UnLocked" % sn

        for k in range(2):
            # test lock btn
            opt_case.check_single_device(sn)
            self.page.select_device(sn)
            self.page.click_lock()
            self.page.refresh_page()
            # check if device lock already
            now_time = self.page.get_current_time()
            while True:
                if "Locked" in opt_case.get_single_device_list(sn)[0]["Lock Status"]:
                    break
                if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                    assert False, "@@@@信息发送失败，请检查！！！！"
                self.page.refresh_page()
                self.page.time_sleep(1)

            self.page.refresh_page()

            opt_case.get_single_device_list(sn)
            self.page.select_device(sn)
            self.page.click_unlock()
            self.page.refresh_page()
            now_time = self.page.get_current_time()
            for j in range(5):
                if "Normal" in opt_case.get_single_device_list(sn)[0]["Lock Status"]:
                    break
                if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                    assert False, "@@@@信息发送失败，请检查！！！！"
                self.page.refresh_page()
                self.page.time_sleep(1)

    @allure.feature('MDM_test02')
    @allure.title("Devices- reboot device 5 times")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_reboot_single_device_pressure_testing(self):
        exp_reboot_text = "Sending Reboot Comand to Devices"
        sn = "A250900P03100019"
        self.page.refresh_page()
        for i in range(2):
            opt_case.check_single_device(sn)
            self.page.select_device(sn)
            self.page.click_reboot_btn()
            case_pack.time.sleep(3)
            self.page.refresh_page()
            # get device info
            # check if command trigger in 3s
            assert "Off" in opt_case.get_single_device_list(sn)[0]["Status"]

            self.page.time_sleep(150)
            self.page.refresh_page()
            assert "On" in opt_case.get_single_device_list(sn)[0]["Status"], "@@@@ 1分钟之内无法重启！！"
            print("成功运行 %s 次" % str(i))

    @allure.feature('MDM_test02')
    @allure.title("Devices- cat_logs")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_cat_logs(self):
        exp_log_msg = "Device Debug Command sent"
        sn = "A250900P03100019"
        self.page.refresh_page()
        opt_case.check_single_device(sn)
        self.page.click_dropdown_btn()
        self.page.click_cat_log()

    @allure.feature('MDM_test02')
    @allure.title("Devices- reset device TPUI password")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_reset_TPUI_password(self):
        exp_psw_text = "Password changed"
        sn = "A250900P03100019"
        password = ["123456", "000000", "999999"]
        self.page.refresh_page()
        self.page.refresh_page()
        for psw in password:
            opt_case.check_single_device(sn)
            self.page.select_device(sn)
            self.page.click_psw_btn()
            self.page.change_TPUI_password(psw)
            self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("Devices- AIMDM send msg and check the log in the Message Module")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_pressure_send_message_to_single_device(self, go_to_and_return_device_page):
        exp_success_send_text = "Message Sent"
        # sn would change after debug with devices
        sn = "A250900P03100019"
        length = 2
        self.page.refresh_page()
        # confirm if device is online and execute next step, if not, end the case execution
        data = opt_case.check_single_device(sn)
        print(data)
        # get device category
        device_cate = data[0]['Category']
        now = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(case_pack.time.time()))
        message_list = []
        for i in range(length):
            self.page.refresh_page()
            msg = "%s: test send message %d" % (now, i)
            opt_case.check_single_device(sn)
            self.page.select_device(sn)
            self.page.click_send_btn()
            self.page.msg_input_and_send(msg)
            message_list.append(msg)

        self.page.go_to_new_address("message")
        # check if Page loaded completely
        self.meg_page.page_load_complete()
        # Check result of device message in the Message Module and msg status
        self.meg_page.choose_device(sn, device_cate)
        now_time = self.page.get_current_time()
        res = self.meg_page.get_device_message_list(now)
        print(res)

        # while True:
        #     msg_list = self.meg_page.get_device_message_list(now)
        #     if len(msg_list) == length:
        #         break
        #     if self.page.get_current_time() > self.page.return_end_time(now_time):
        #         assert False, "@@@终端收到信息后, 平台180s内无法收到相应的信息"
        #     self.page.time_sleep(1)

    @allure.feature('MDM_test02')
    @allure.title("Devices- AIMDM transfer api server ")
    @pytest.mark.flaky(reruns=5, reruns_delay=3)
    def test_transfer_api_server(self):
        exp_success_msg = "Updated Device Setting"
        test_version_api = "http://test.telpopaas.com"
        release_version_api = "http://api.telpotms.com"
        release_version_url = "https://mdm.telpoai.com/login"
        release_user_info = {"username": "ceshibu03", "password": "123456"}
        sn = "A250900P03100019"
        release_main_title = "Total Devices"
        release_login_ok_title = "Telpo MDM"
        self.page.refresh_page()
        self.page.page_load_complete()

        case_pack.BaseWebDriver().open_web_site(release_version_url)
        release_driver = case_pack.BaseWebDriver().get_web_driver()
        release_page = case_pack.ReleaseDevicePage(release_driver, 40)

        opt_case.check_single_device(sn)
        self.page.select_device(sn)
        self.page.click_server_btn()
        self.page.api_transfer(release_version_api)
        # time.sleep(150)
        # check if device is offline in test version
        self.page.refresh_page()
        test_device_info = opt_case.get_single_device_list(sn)
        print(test_device_info)

        # go to release version and check if device is online
        release_page.refresh_page()
        release_page.login_release_version(release_user_info, release_login_ok_title)
        release_page.go_to_device_page(release_main_title)
        release_data_list = release_page.get_single_device_list_release(sn)
        print(release_data_list)

        # if release_data_list[0]["Status"] == "Off":
        #     assert False

        release_page.select_device(sn)
        release_page.click_server_btn()
        release_page.api_transfer(test_version_api)

        # time.sleep(150)
        # check if device is offline in release version
        release_page.refresh_page()
        release_data_info_again = release_page.get_single_device_list_release(sn)
        print(release_data_info_again)
        # if release_data_list[0]["Status"] == "On":
        #     assert False
        release_page.quit_browser()

        # go to test version and check if device is online
        self.page.refresh_page()
        test_data_info = opt_case.get_single_device_list(sn)
        print(test_data_info)
        # if release_data_list[0]["Status"] == "Off":
        #     assert False

    @allure.feature('MDM_test01')
    @allure.title("Devices- device shutdown -- test in the last")
    def test_device_shutdown(self):
        sn = "A250900P03100019"
        exp_shutdown_text = "Device ShutDown Command sent"
        opt_case.check_single_device(sn)
        self.page.click_dropdown_btn()
        self.page.click_shutdown_btn()
        # check if shutdown command works in 3 sec
        self.page.time_sleep(3)
        self.page.refresh_page()
        assert "Off" in opt_case.get_single_device_list(sn)[0]["Status"]

    @allure.feature('MDM_test01')
    @allure.title("Devices-debug")
    def test_devices_test(self):
        sn = "A250900P03100019"
        length = 3
        message_page_title = "Device Message"
        self.telpo_mdm_page.click_message_btn()
        if not (message_page_title in self.meg_page.get_loc_main_title()):
            self.telpo_mdm_page.click_message_btn()
        case_pack.time.sleep(1)
        self.meg_page.choose_device(sn, "壁挂式")
        msg_list = self.meg_page.get_device_message_list(length)
        print(msg_list)
        case_pack.time.sleep(4)
