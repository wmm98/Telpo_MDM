import Page as public_pack
from Page.Telpo_MDM_Page import TelpoMDMPage

By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time
log = public_pack.MyLog()
conf = public_pack.Config()


class ContentPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_content_list = (By.ID, "fgdata")
    loc_single_content = (By.CLASS_NAME, "fg-file")
    loc_content_detail_btn = (By.CSS_SELECTOR, "[class = 'fas fa-list-ul']")
    loc_detail_box = (By.CLASS_NAME, "fd-panel-detail")
    loc_detail_release_btn = (By.CSS_SELECTOR, "[class = 'fas fa-registered']")
    # release btn related
    loc_content_release_alert = (By.ID, "modal-release")
    loc_device_list = (By.ID, "snlist")
    loc_single_device = (By.TAG_NAME, "li")
    loc_content_release_confirm = (By.CSS_SELECTOR, "[class = 'btn btn-danger btn-release']")

    # search related
    loc_search_box_show = (By.CSS_SELECTOR,
                           "[class = 'btn btn-tool btn-searchbar']")  # open status  display: inline-block;  default status: display: none;
    loc_content_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_files_type = (By.CSS_SELECTOR, "[class = 'form-control form-control-sm file-search-usefor']")
    loc_input_name_box = (By.CSS_SELECTOR, "[class = 'form-control file-search-name']")

    # add content file relate
    loc_new_file = (By.CSS_SELECTOR, "[class = 'fas fa-plus']")
    loc_user_for_box = (By.CLASS_NAME, "fs-use-bar")
    loc_use_files = (By.CLASS_NAME, "fs-use-file")
    loc_upload_content_btn = (By.CSS_SELECTOR, "[class = 'fas fa-cloud-upload-alt']")
    loc_upload_save = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-submit']")

    # alert show
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")
    loc_show_device_btn = (By.CSS_SELECTOR, "[class = 'btn btn-sm bg-teal show-labelitem']")

    # content release Page
    loc_release_check_all = (By.ID, "checkall")
    loc_release_delete_btn = (By.CSS_SELECTOR, "[class = 'fas fa-trash-alt']")
    loc_release_confirm_del_btn = (By.CSS_SELECTOR, "[class = 'btn btn-danger btn-dels']")
    loc_release_list = (By.ID, "databody")
    loc_single_release = (By.TAG_NAME, "tr")
    loc_single_release_col = (By.TAG_NAME, "td")
    loc_release_path = (By.ID, "device_path")

    # content upgrade logs relate
    loc_app_upgrade_logs_body = (By.ID, "databody")
    loc_app_upgrade_single_log = (By.TAG_NAME, "tr")
    loc_app_upgrade_log_col = (By.TAG_NAME, "td")
    loc_upgrade_search_sn_box = (By.ID, "sn")
    loc_upgrade_search_ensure = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-search']")

    # category relate
    loc_new_cate_btn = (By.LINK_TEXT, "Create New Category")
    loc_input_cate_box = (By.ID, "categoryname")
    loc_save_btn_cate = (By.CSS_SELECTOR, "[class = 'btn btn-primary category_submit']")
    loc_cate_list = (By.CSS_SELECTOR, "[class = 'todo-list ui-sortable category-ul']")
    loc_single_cate = (By.CLASS_NAME, "listactive")

    def new_content_category(self, cate_name):
        # add category
        self.click(self.loc_new_cate_btn)
        self.confirm_alert_existed(self.loc_new_cate_btn)
        self.input_text(self.loc_input_cate_box, cate_name)
        self.click(self.loc_save_btn_cate)
        self.confirm_tips_alert_show(self.loc_save_btn_cate)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    def get_content_categories_list(self):
        if self.ele_is_existed(self.loc_cate_list):
            if self.ele_is_existed(self.loc_cate_list):
                eles = self.get_elements(self.loc_single_cate)
                cates_list = [self.remove_space(ele.text) for ele in eles]
                return cates_list
            else:
                return []
        else:
            return []

    def add_content_file(self, file_type, file_path):
        # file_type
        # normal_file, boot_animation wallpaper, logo
        self.click(self.loc_new_file)
        self.confirm_alert_existed(self.loc_alert_show, self.loc_new_file)
        uses_for = self.get_element(self.loc_user_for_box).find_elements(*self.loc_use_files)
        if file_type == "normal_file":
            uses_for[0].click()
        elif file_type == "boot_animation":
            uses_for[1].click()
        elif file_type == "wallpaper":
            uses_for[2].click()
        elif file_type == "logo":
            uses_for[3].click()
        self.input_text(self.loc_upload_content_btn, file_path)
        self.click(self.loc_upload_save)
        self.confirm_tips_alert_show(self.loc_upload_save)
        self.refresh_page()

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

    def search_upgrade_log_by_sn(self, sn):
        try:
            self.time_sleep(3)
            self.click(self.loc_content_search_btn)
            self.time_sleep(2)
            self.confirm_alert_existed(self.loc_alert_show, self.loc_content_search_btn)
            self.input_text(self.loc_upgrade_search_sn_box, sn)
            self.time_sleep(1)
            self.click(self.loc_upgrade_search_ensure)
            self.time_sleep(2)
            self.confirm_alert_not_existed(self.loc_upgrade_search_ensure)
        except Exception as e:
            print(e)
            # self.refresh_page()
            # self.click(self.loc_content_search_btn)
            # self.confirm_alert_existed(self.loc_alert_show, self.loc_content_search_btn)
            # self.input_text(self.loc_upgrade_search_sn_box, sn)
            # self.time_sleep(1)
            # self.click(self.loc_upgrade_search_ensure)
            # self.confirm_alert_not_existed(self.loc_upgrade_search_ensure)

    def get_content_latest_upgrade_log(self, send_time, release_info):
        try:
            logs_list = []
            if self.ele_is_existed_in_range(self.loc_app_upgrade_logs_body, self.loc_app_upgrade_single_log):
                upgrade_list = self.get_element(self.loc_app_upgrade_logs_body)
                if self.remove_space("No Data") in self.remove_space(upgrade_list.text):
                    return []
                single_log = upgrade_list.find_elements(*self.loc_app_upgrade_single_log)[0]
                cols = single_log.find_elements(*self.loc_app_upgrade_log_col)
                receive_time_text = cols[-2].text
                sn = cols[-3].text
                action = cols[-1].text
                file_name = cols[0].text
                time_line = self.extract_integers(receive_time_text)
                receive_time = self.format_string_time(time_line)
                if self.compare_time(send_time, receive_time):
                    if (release_info["sn"] in sn) and (release_info["content_name"] in file_name):
                        logs_list.append({"SN": sn, "Update Time": receive_time, "Action": action})
                return logs_list
            else:
                return []
        except Exception:
            return []

    def delete_all_content_release_log(self):
        self.go_to_new_address("content/release")
        try:
            if self.get_current_content_release_log_total() != 0:
                self.click_select_all_box()
                self.click_delete_btn()
                self.refresh_page()
        except Exception:
            self.refresh_page()
            if self.get_current_content_release_log_total() != 0:
                self.click_select_all_box()
                self.click_delete_btn()
                self.refresh_page()

    def get_current_content_release_log_total(self):
        release_list = self.get_element(self.loc_release_list)
        if self.remove_space("No Data") in self.remove_space(release_list.text):
            return 0
        release_count = len(release_list.find_elements(*self.loc_single_release))
        return release_count

    def click_select_all_box(self):
        ele = self.get_element(self.loc_release_check_all)
        self.exc_js_click(ele)
        self.deal_ele_selected(ele)

    def click_delete_btn(self):
        self.click(self.loc_release_delete_btn)
        self.confirm_alert_existed(self.loc_release_delete_btn)
        self.click(self.loc_release_confirm_del_btn)
        self.confirm_tips_alert_show(self.loc_release_confirm_del_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_release_confirm_del_btn)

    def get_content_latest_release_log_list(self, send_time, release_info):
        try:
            release_list = self.get_element(self.loc_release_list)
            logs_list = []
            if self.remove_space("NO Data") in self.remove_space(release_list.text):
                return []
            logs = release_list.find_elements(*self.loc_single_release)
            for single_log in logs:
                cols = single_log.find_elements(*self.loc_single_release_col)
                receive_time_text = cols[-1].text
                sn = cols[-3].text
                file_name = cols[1].text
                time_line = self.extract_integers(receive_time_text)
                receive_time = self.format_string_time(time_line)
                if self.compare_time(send_time, receive_time):
                    if (release_info["sn"] in sn) and (release_info["content_name"] in file_name):
                        logs_list.append(single_log)
            return logs_list
        except Exception:
            return []

    def release_content_file(self, sn, file_path=False):
        self.show_detail_box()
        self.input_release_content_info(sn, file_path)

    def show_detail_box(self):
        self.click(self.loc_content_detail_btn)
        self.confirm_detail_box_show()
        release_btn = self.get_element(self.loc_detail_box).find_element(*self.loc_detail_release_btn)
        release_btn.click()
        self.confirm_alert_existed(self.loc_detail_release_btn)

    def input_release_content_info(self, sn_, file_path):
        if file_path:
            self.input_text(self.loc_release_path, file_path)
        release_box = self.get_element(self.loc_content_release_alert)
        # click show devices btn， check if device is show, if now, click it
        btn = self.get_element(self.loc_show_device_btn)
        if "block" in btn.get_attribute("style"):
            btn.click()
        devices = release_box.find_element(*self.loc_device_list).find_elements(*self.loc_single_device)
        if isinstance(sn_, list):
            for sn in sn_:
                for device in devices:
                    if sn in device.get_attribute("data"):
                        if device.get_attribute("class") == "selected":
                            break
                        self.confirm_sn_is_selected(device)
        else:
            for device in devices:
                if sn_ in device.get_attribute("data"):
                    if device.get_attribute("class") == "selected":
                        break
                    self.confirm_sn_is_selected(device)
        self.click(self.loc_content_release_confirm)
        self.confirm_tips_alert_show(self.loc_content_release_confirm)
        self.refresh_page()
        # self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_content_release_confirm)

    def confirm_detail_box_show(self):
        now_time = self.get_current_time()
        while True:
            if "block" in self.get_element(self.loc_detail_box).get_attribute("style"):
                break
            else:
                self.click(self.loc_content_detail_btn)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@无法打开content detail, 请检查！！！"
            self.time_sleep(1)

    def search_content(self, f_type, f_name):
        try:
            self.time_sleep(3)
            search_ele = self.get_element(self.loc_search_box_show).find_element(*self.loc_content_search_btn)
            search_ele.click()
            # self.exc_js_click(search_ele)
            self.confirm_search_box_show()
            self.select_file_type(f_type)
            self.input_text(self.loc_input_name_box, f_name)
            self.time_sleep(1)
            self.input_keyboard(self.loc_input_name_box, public_pack.Keys.ENTER)
        except public_pack.ElementNotInteractableException:
            search_ele = self.get_element(self.loc_search_box_show).find_element(*self.loc_content_search_btn)
            # .find_element(*self.loc_search_btn)
            search_ele.click()
            self.time_sleep(3)
            self.confirm_search_box_show()
            self.select_file_type(f_type)
            self.input_text(self.loc_input_name_box, f_name)
            self.time_sleep(1)
            self.input_keyboard(self.loc_input_name_box, public_pack.Keys.ENTER)

    def select_file_type(self, file_type):
        self.select_by_text(self.loc_files_type, file_type)

    def get_content_list(self):
        if "NO Data" in self.get_element(self.loc_content_list).text:
            return []
        else:
            boxes = self.get_elements_in_range(self.loc_content_list, self.loc_single_content)
            return boxes

    def confirm_search_box_fade(self):
        now_time = self.get_current_time()
        while True:
            if "inline-block" in self.get_element(self.loc_search_box_show).get_attribute("style"):
                break
            else:
                self.ele_is_existed_in_range(self.loc_search_box_show, self.loc_content_search_btn)
                ele = self.get_element(self.loc_search_box_show).find_element(self.loc_content_search_btn)
                ele.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法打开搜索框， 请检查！！！！"
            self.time_sleep(1)

    def confirm_search_box_show(self):
        now_time = self.get_current_time()
        while True:
            if "none" in self.get_element(self.loc_search_box_show).get_attribute("style"):
                break
            else:
                self.ele_is_existed_in_range(self.loc_search_box_show, self.loc_content_search_btn)
                ele = self.get_element(self.loc_search_box_show).find_element(self.loc_content_search_btn)
                ele.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法进行搜索， 请检查！！！！"
            self.time_sleep(1)
