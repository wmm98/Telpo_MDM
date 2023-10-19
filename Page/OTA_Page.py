import Page as public_pack
from Page.Telpo_MDM_Page import TelpoMDMPage

conf = public_pack.Config()
By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time


class OTAPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_upgrade_packages_btn = (By.LINK_TEXT, "Upgrade Packages")
    upgrade_package_main_title = "OTA"

    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_input_search_package = (By.ID, "searchname")
    loc_search_category = (By.ID, "searchcate")
    loc_search_search_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-search']")

    # delete ota package btn relate
    loc_delete_ota_package_btn = (By.CSS_SELECTOR, "[class = 'fas fa-trash-alt']")
    loc_delete_ota_package_confirm = (By.CSS_SELECTOR, "[class = 'btn btn-danger btn-del']")

    # add OTA package btn relate
    loc_add_package_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square']")
    loc_choose_package_btn = (By.ID, "customFile")
    loc_file_category = (By.ID, "cid")
    loc_android_checkbox = (By.ID, "customRadio1")
    loc_linux_checkbox = (By.ID, "customRadio2")
    loc_save_package_info_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-submit']")
    loc_uploading_show = (By.CSS_SELECTOR, "[class = 'modal-backdrop fade show']")

    # search alert
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade modal_dark show']")

    # package box relate  upgrade package
    loc_packages_box = (By.CSS_SELECTOR, "[class = 'col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column']")
    loc_release_btn = (By.CSS_SELECTOR, "[class = 'btn btn-sm bg-teal btn-release-model']")
    loc_silent_update = (By.ID, "issilent")
    loc_download_network = (By.ID, "download_network")
    loc_dev_cate = (By.ID, "devcate")
    loc_show_device_btn = (By.CSS_SELECTOR, "[class = 'btn btn-sm bg-teal show-labelitem']")
    loc_hide_device_btn = (By.CSS_SELECTOR, "[class = 'btn btn-sm bg-teal hide-labelitem']")
    loc_release_package_btn = (By.CSS_SELECTOR, "[class = 'btn btn-danger btn-release']")
    loc_sn_list = (By.ID, "snlist")
    loc_sn_text = (By.TAG_NAME, "li")
    loc_label_selected = (By.CLASS_NAME, "label-selected")

    loc_ota_list = (By.ID, "otalist")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")

    # package release module relate
    loc_package_releases_btn = (By.LINK_TEXT, "Package Releases")
    ota_release_package_title = "OTA Package Releases"
    loc_data_body = (By.ID, "databody")
    loc_single_log = (By.TAG_NAME, "tr")
    loc_single_release_col = (By.TAG_NAME, "td")
    # delete btn relate
    loc_release_delete_btn = (By.CSS_SELECTOR, "[class = 'fas fa-trash-alt']")
    loc_release_confirm_del = (By.CSS_SELECTOR, "[class = 'btn btn-danger btn-dels']")
    loc_send_release_again_btn = (By.CSS_SELECTOR, "[class = 'btn-witdh btn  btn-sm sync_release']")

    loc_release_search_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-search-model']")
    loc_search_release_package_name = (By.ID, "packagename")
    loc_search_release_sn = (By.ID, "sn")
    loc_search_release_search = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-search']")
    loc_log_check_box = (By.NAME, "checkbox")

    # select_all
    loc_release_check_all = (By.ID, "checkall")

    # ota upgrade logs relate
    loc_app_upgrade_logs_body = (By.ID, "databody")
    loc_app_upgrade_single_log = (By.TAG_NAME, "tr")
    loc_app_upgrade_log_col = (By.TAG_NAME, "td")

    def get_ota_latest_upgrade_log(self, send_time, release_info):
        self.page_load_complete()
        self.time_sleep(2)
        upgrade_list = self.get_element(self.loc_app_upgrade_logs_body)
        logs_list = []
        if "No Data" in upgrade_list.text:
            return []
        if self.ele_is_existed_in_range(self.loc_app_upgrade_logs_body, self.loc_app_upgrade_single_log):
            single_log = upgrade_list.find_elements(*self.loc_app_upgrade_single_log)[0]
            cols = single_log.find_elements(*self.loc_app_upgrade_log_col)
            receive_time_text = cols[4].text
            sn = cols[0].text
            action = cols[5].text
            package = cols[1].text
            version = cols[3].text
            time_line = self.extract_integers(receive_time_text)
            receive_time = self.format_string_time(time_line)
            if self.compare_time(send_time, receive_time):
                if (release_info["sn"] in sn) and (release_info["package_name"] in package):
                    if release_info["version"] in version:
                        logs_list.append({"SN": sn, "Update Time": receive_time, "Action": action, "Version": version})
            return logs_list
        else:
            return []

    def click_select_all_box(self):
        ele = self.get_element(self.loc_release_check_all)
        self.exc_js_click(ele)
        self.deal_ele_selected(ele)

    def click_delete_release_btn(self):
        self.click(self.loc_release_delete_btn)
        self.confirm_alert_existed(self.loc_release_delete_btn)
        self.click(self.loc_release_confirm_del)
        self.confirm_tips_alert_show(self.loc_release_confirm_del)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_release_confirm_del)

    def delete_all_ota_release_log(self):
        try:
            if self.get_current_ota_release_log_total() != 0:
                self.click_select_all_box()
                self.click_delete_release_btn()
                self.refresh_page()
        except Exception:
            self.refresh_page()
            if self.get_current_ota_release_log_total() != 0:
                self.click_select_all_box()
                self.click_delete_release_btn()
                self.refresh_page()

    def get_current_ota_release_log_total(self):
        self.page_load_complete()
        release_list = self.get_element(self.loc_data_body)
        if "No Data" in release_list.text:
            return 0
        is_exited = self.ele_is_existed_in_range(self.loc_data_body, self.loc_single_log)
        if is_exited:
            self.time_sleep(2)
            is_exited = self.ele_is_existed_in_range(self.loc_data_body, self.loc_single_log)
        if is_exited:
            release_count = len(release_list.find_elements(*self.loc_single_log))
            return release_count
        else:
            return 0

    def get_ota_latest_release_log_list(self, send_time, release_info):
        self.page_load_complete()
        try:
            release_list = self.get_element(self.loc_data_body)
            logs_list = []
            existed = self.ele_is_existed_in_range(self.loc_data_body, self.loc_single_log)
            if not existed:
                self.time_sleep(2)
                existed = self.ele_is_existed_in_range(self.loc_data_body, self.loc_single_log)
            if "No Data" in release_list.text:
                return []
            if existed:
                logs = release_list.find_elements(*self.loc_single_log)
                for single_log in logs:
                    cols = single_log.find_elements(*self.loc_single_release_col)
                    receive_time_text = cols[4].text
                    sn = cols[6].text
                    package = cols[1].text
                    version = cols[3].text
                    time_line = self.extract_integers(receive_time_text)
                    receive_time = self.format_string_time(time_line)
                    if self.compare_time(send_time, receive_time):
                        if (release_info["sn"] in sn) and (release_info["package_name"] in package):
                            if release_info["version"] in version:
                                logs_list.append(single_log)
                print(logs_list)
                print(len(logs_list))
                return logs_list
            else:
                return []
        except Exception as e:
            return []

    def delete_ota_package(self):
        self.click(self.loc_delete_ota_package_btn)
        self.confirm_alert_existed(self.loc_delete_ota_package_btn)
        self.click(self.loc_delete_ota_package_confirm)
        self.confirm_tips_alert_show(self.loc_delete_ota_package_confirm)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_delete_ota_package_confirm)

    def click_package_release_page(self):
        self.click(self.loc_package_releases_btn)
        now_time = self.get_current_time()
        while True:
            if self.ota_release_package_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_package_releases_btn)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@ 打开package release 出错！！！"
            self.time_sleep(1)

    def get_release_log_length(self):
        body_list = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_data_body))
        log_list = body_list.find_elements(*self.loc_single_log)
        if "No Data" in body_list.text:
            return 0
        else:
            return len(log_list)

    def get_releases_log_text(self):
        log_body = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_data_body))
        log_list = log_body.find_elements(*self.loc_single_log)
        log_text = [log.text for log in log_list]
        return log_text

    def check_single_release_info(self, release_info):
        if self.get_release_log_length() == 0:
            assert False, "@@@@没有OTA release的记录， 请检查！！！"
        logs_text = self.get_releases_log_text()
        for log_txt in logs_text:
            if not release_info["package_name"] in log_txt and release_info["sn"] in log_txt:
                assert False, "@@@@没有%s, %s 的release记录， 请检查！！！" % (release_info["package_name"], release_info["sn"])

    def search_single_release_log(self, info, count=True):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_release_search_btn))
        self.click(self.loc_release_search_btn)
        self.confirm_alert_existed(self.loc_release_search_btn)
        self.input_text(self.loc_search_release_package_name, info["package_name"])
        self.input_text(self.loc_search_release_sn, info["sn"])
        self.time_sleep(1)
        self.click(self.loc_search_release_search)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_release_search)

        if count:
            if "NO Data" in self.get_element(self.loc_data_body).text:
                assert False, "@@@@找不到此包 %s %s 的release 记录, 请检查！！！" % (info["package_name"], info["sn"])

            # boxes = self.get_elements(self.loc_packages_box)
            # if len(boxes) != 1:
            #     assert False, "@@@@有多个相同的  %s %s 释放记录, 请检查！！！" % (info["package_name"], info["sn"])

    def release_again(self):
        self.click(self.loc_send_release_again_btn)
        self.confirm_tips_alert_show(self.loc_send_release_again_btn)

    def delete_all_release_log(self, org_len=0, del_all=True):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_release_check_all))
        self.exc_js_click_loc(self.loc_release_check_all)
        self.deal_ele_selected(ele)
        self.click(self.loc_release_delete_btn)
        self.confirm_alert_existed(self.loc_release_delete_btn)
        self.click(self.loc_release_confirm_del)
        self.confirm_alert_not_existed(self.loc_release_confirm_del)
        # self.refresh_page()
        if del_all:
            while True:
                now_time = self.get_current_time()
                if self.get_release_log_length() == 0:
                    break
                else:
                    self.exc_js_click_loc(self.loc_release_check_all)
                    self.deal_ele_selected(ele)
                    self.click(self.loc_release_delete_btn)
                    self.confirm_alert_existed(self.loc_release_delete_btn)
                self.time_sleep(1)
                if self.get_current_time() > self.return_end_time(now_time):
                    assert False, "@@@@删除全部release ota logs 出错, 请检查！！！"
        else:
            while True:
                if org_len == (self.get_release_log_length() + 1):
                    break
                else:
                    self.exc_js_click_loc(self.loc_release_check_all)
                    self.deal_ele_selected(ele)
                    self.click(self.loc_release_delete_btn)
                    self.confirm_alert_existed(self.loc_release_delete_btn)
                self.time_sleep(1)

    def select_release_log(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_log_check_box))
        self.exc_js_click_loc(self.loc_log_check_box)
        self.deal_ele_selected(ele)

    def click_upgrade_packages(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_upgrade_packages_btn))
        self.click(self.loc_upgrade_packages_btn)
        now_time = self.get_current_time()
        while True:
            if self.upgrade_package_main_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_upgrade_packages_btn)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@ 打开upgrade packages 出错！！！"

    def get_package_ele_discard(self, pack_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_packages_box))
        eles = self.get_elements(self.loc_packages_box)
        for ele in eles:
            if pack_name in ele.text:
                return ele

    def click_release_btn(self):
        self.click(self.loc_release_btn)
        self.confirm_alert_existed(self.loc_release_btn)

    def input_release_OTA_package(self, release_info):
        # {"network": "NO Limit", "silent": 0, "category": "No Limit"}
        self.select_by_text(self.loc_download_network, release_info['network'])
        silent_update = self.get_element(self.loc_silent_update)
        if release_info["silent"] == 1:
            self.exc_js_click(silent_update)
        self.select_by_text(self.loc_dev_cate, release_info["category"])
        # click show devices btn， check if device is show, if now, click it
        btn = self.get_element(self.loc_show_device_btn)
        if "block" in btn.get_attribute("style"):
            btn.click()
        sn_list = self.get_element(self.loc_sn_list)
        eles_sn = sn_list.find_elements(*self.loc_sn_text)
        for ele_sn in eles_sn:
            if release_info["sn"] in ele_sn.text:
                if ele_sn.get_attribute("class") == "selected":
                    break
                self.confirm_sn_is_selected(ele_sn)
        self.exc_js_click(self.get_element(self.loc_release_package_btn))
        self.confirm_tips_alert_show(self.loc_release_package_btn, ex_js=1)
        self.refresh_page()
        # self.confirm_alert_not_existed(self.loc_release_package_btn, ex_js=1)

    def click_alert_release_btn(self):
        # self.click(self.loc_release_package_btn)
        # print("弹窗是否存在：", self.alert_is_existed())
        try:
            self.exc_js_click(self.get_element(self.loc_release_package_btn))
            self.confirm_tips_alert_show(self.loc_release_package_btn, ex_js=1)
        except Exception:
            self.confirm_alert_not_existed(self.loc_release_package_btn, ex_js=1)

    def search_device_by_pack_name(self, pack_name):
        try:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_input_search_package, pack_name)
            self.time_sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)
        except public_pack.ElementNotInteractableException:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_input_search_package, pack_name)
            self.time_sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)

    def get_ota_package_list(self):
        if "NO Data" in self.get_element(self.loc_ota_list).text:
            return []
        else:
            boxes = self.get_elements(self.loc_packages_box)
            return boxes

    def click_add_btn(self):
        self.click(self.loc_add_package_btn)
        self.confirm_alert_existed(self.loc_add_package_btn)

    def input_ota_package_info(self, info):
        self.input_text(self.loc_choose_package_btn, info["file_name"])
        self.select_by_text(self.loc_file_category, info["file_category"])
        android_check_box = self.get_element(self.loc_android_checkbox)
        linux_check_box = self.get_element(self.loc_linux_checkbox)
        if info["plat_form"] == "Android":
            if not android_check_box.is_selected():
                android_check_box.click()
        elif info["plat_form"] == "Linux":
            if not linux_check_box.is_selected():
                linux_check_box.click()

    def click_save_add_ota_pack(self):
        self.click(self.loc_save_package_info_btn)
        now_time = t_time.time()
        while True:
            if self.uploading_box_show():
                break
            else:
                self.click(self.loc_save_package_info_btn)
            if t_time.time() > self.return_end_time(now_time):
                assert False, "@@@@无法上传OTA， 请检查！！！"
            self.time_sleep(1)
        # if not self.uploading_box_fade():
        #     print("333333333333333333333333333333333333")
        #     assert False, "@@@@上传OTA文件超过3分钟， 请检查！！！！"
        if not self.get_tips_alert(180):
            assert False, "@@@@上传OTA文件超过3分钟， 请检查！！！！"

    def uploading_box_show(self):
        try:
            self.web_driver_wait_until(EC.visibility_of_element_located(self.loc_uploading_show))
            return True
        except public_pack.TimeoutException:
            return False

    def uploading_box_fade(self):
        try:
            self.web_driver_wait_until_not(EC.visibility_of_element_located(self.loc_uploading_show), 180)
            return True
        except public_pack.TimeoutException:
            return False

    # check if alert would disappear
    def alert_fade(self):
        try:
            self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 6)
            return True
        except public_pack.TimeoutException:
            return False

    # check if alert would appear
    def alert_show(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 6)
            return True
        except public_pack.TimeoutException:
            return False

    def confirm_tips_alert_show(self, loc, ex_js=0, times=0):
        now_time = self.get_current_time()
        while True:
            if self.get_tips_alert(times):
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭，请检查！！！"
            self.time_sleep(1)

    def get_tips_alert(self, timeout=0):
        try:
            if timeout != 0:
                ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed), timeout)
                print(ele.text)
            else:
                ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed), 5)
                print(ele.text)
            return True
        except public_pack.TimeoutException:
            return False
