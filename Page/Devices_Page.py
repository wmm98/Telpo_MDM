from selenium.common import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from Conf.Config import Config
from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time

conf = Config()


class DevicesPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    # Devices_list btn  --new add for test version
    loc_devices_list_btn = (By.LINK_TEXT, "Devices List")

    loc_category_btn = (By.LINK_TEXT, "Create New Category")
    loc_input_cate_box = (By.ID, "category_name")
    loc_save_btn_cate = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_category_button']")
    loc_close_btn_cate = (By.XPATH, "//*[@id=\"modal-add-category\"]/div/div/div[3]/button[1]")

    loc_mode_btn = (By.LINK_TEXT, "Create New Model")
    loc_input_mode_box = (By.ID, "model_name")
    loc_save_btn_mode = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_model_button']")
    loc_close_btn_mode = (By.XPATH, "//*[@id=\"modal-add-model\"]/div/div/div[3]/button[1]")
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")
    loc_mode_name_success = (By.ID, "swal2-title")

    # Model盒子,model list
    loc_models_box = (By.CSS_SELECTOR, "[class = 'modelSelectd model_list']")

    # 种类text
    loc_cate_box = (By.CLASS_NAME, "category_list")

    # New device btn relate
    loc_new_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square text-black']")
    loc_input_dev_name = (By.ID, "device_name")
    loc_input_dev_SN = (By.ID, "device_sn")
    loc_select_dev_cate = (By.ID, "Category")
    loc_select_dev_mode = (By.ID, "Model")
    loc_save_dev_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_create_device_button']")
    loc_close_dev_btn = (By.XPATH, "//*[@id=\"modal-add-device\"]/div/div/div[3]/button[1]")
    loc_add_device_success_warning = (By.ID, "modal-warning-device-model")
    # 设备列表
    loc_devices_list = (By.ID, "device_list")
    loc_label = (By.TAG_NAME, "label")
    loc_tr = (By.TAG_NAME, "tr")
    loc_td = (By.CLASS_NAME, "text-center")

    # check box
    loc_check_all = (By.ID, "checkall")

    # Import btn relate; import devices
    loc_import_btn = (By.CSS_SELECTOR, "[class = 'fas fa-file-upload batch_upload_device']")
    loc_download_template_btn = (By.LINK_TEXT, "Download Template Here")
    loc_choose_file_btn = (By.ID, "file")
    loc_import_cate_btn = (By.ID, "import_Category")
    loc_import_model_btn = (By.ID, "import_Model")
    loc_import_company_btn = (By.ID, "import_subcompany")
    loc_import_save_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_import_device_button']")
    # just for find the close-btn
    loc_import_devices_box = (By.ID, "modal-import-device")
    loc_import_close_btn = (By.CSS_SELECTOR, "[class = 'btn btn-default']")
    file_path = conf.project_path + "\\Param\\device import.xlsx"

    # send message
    loc_msg_btn = (By.CSS_SELECTOR, "[class = 'fas fa-envelope batch_message']")
    loc_msg_input_box = (By.ID, "device_notification")
    loc_msg_input_send_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_send_device_message']")
    loc_msg_input_close_btn_large = (By.ID, "modal-device-message")  # just for serach the exact close btn
    loc_msg_input_close_btn = (By.CSS_SELECTOR, "[class = 'btn btn-default']")

    # search device(sn)
    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_search_input_box = (By.ID, "search_device_sn")
    loc_search_search_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_search_device_button']")

    # lock and unlock btn  relate
    loc_lock_btn = (By.CSS_SELECTOR, "[class = 'fas fa-lock batch_lock']")
    loc_unlock_btn = (By.CSS_SELECTOR, "[class = 'fas fa-lock-open batch_unlock']")

    # reboot btn relate
    loc_reboot_btn = (By.CSS_SELECTOR, "[class = 'fas fa-retweet batch_reboot']")
    loc_sure_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-dark sure_batch_reboot']")
    loc_warning = (By.ID, "modal-device-reboot-message")

    # Action button relate
    # shutdown btn
    loc_dropdown_btn = (By.CSS_SELECTOR, "[class = 'btn btn-warning dropdown-toggle dropdown-icon']")
    loc_menu_show = (By.CSS_SELECTOR, "[class = 'dropdown-menu dropdown-menu-right show']")
    loc_shutdown_btn = (By.CSS_SELECTOR, "[class = 'fas fa-power-off']")
    loc_shutdown_sure_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-dark sure_command_button']")

    # cat log btn
    loc_cat_log_btn = (By.CSS_SELECTOR, "[class = 'far fa-file-code']")

    # psw btn relate
    loc_psw_btn = (By.CSS_SELECTOR, "[class = 'fas fa-key batch_password']")
    loc_TPUI_password = (By.ID, "device_tpui_password")
    loc_lock_password = (By.ID, "device_password")
    loc_save_psw_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_update_device_password']")

    # server relate
    lco_server_btn = (By.CSS_SELECTOR, "[class = 'fas fa-server batch_api']")
    loc_api_box = (By.ID, "new_api")
    loc_api_send_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary sure_update_server_api']")

    # left bar
    loc_left_bar = (By.CLASS_NAME, "col-md-3")

    def click_server_btn(self):
        self.click(self.lco_server_btn)
        self.confirm_alert_existed(self.lco_server_btn)

    def api_transfer(self, api_url):
        self.input_text(self.loc_api_box, api_url)
        self.click(self.loc_api_send_btn)
        self.confirm_tips_alert_show(self.loc_api_send_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_api_send_btn)

    def click_psw_btn(self):
        self.click(self.loc_psw_btn)
        self.confirm_alert_existed(self.loc_psw_btn)

    def change_TPUI_password(self, psw):
        self.alert_show()
        self.input_text(self.loc_TPUI_password, psw)
        self.click(self.loc_save_psw_btn)
        self.confirm_tips_alert_show(self.loc_save_psw_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_psw_btn)
        # self.alert_fade()

    def click_dropdown_btn(self):
        self.click(self.loc_dropdown_btn)
        now_time = time.time()
        while True:
            if self.ele_is_existed(self.loc_menu_show):
                break
            else:
                self.click(self.loc_dropdown_btn)
            time.sleep(1)
            if time.time() > self.return_end_time(now_time):
                assert False, "@@@@dropdown 按钮无法打开！！！"
        # self.web_driver_wait_until(EC.presence_of_element_located(self.loc_menu_show), 10)

    def click_shutdown_btn(self):
        self.click(self.loc_shutdown_btn)
        self.confirm_alert_existed(self.loc_shutdown_btn)
        self.click(self.loc_shutdown_sure_btn)
        self.confirm_tips_alert_show(self.loc_shutdown_sure_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_shutdown_sure_btn)

    def click_cat_log(self):
        self.click(self.loc_cat_log_btn)
        self.confirm_alert_existed(self.loc_cat_log_btn)
        self.click(self.loc_shutdown_sure_btn)
        self.confirm_tips_alert_show(self.loc_shutdown_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_shutdown_btn)
        # now_time = time.time()
        # while True:
        #     if self.get_tips_alert():
        #         break
        #     else:
        #         self.click(self.loc_shutdown_sure_btn)
        #     if time.time() > self.return_end_time(now_time, 60):
        #         assert False, "@@@@页面点击确认捕捉log失败， 请检查！！！"

    # reboot relate
    def click_reboot_btn(self):
        self.click(self.loc_reboot_btn)
        self.confirm_alert_existed(self.loc_sure_btn)
        self.click(self.loc_sure_btn)
        self.confirm_tips_alert_show(self.loc_sure_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_sure_btn)

    def get_reboot_warning_alert_text(self, text):
        if text in self.get_element(self.loc_warning).text:
            # print(self.get_element(self.loc_warning).text)
            self.refresh_page()
        else:
            self.click(self.loc_sure_btn)
            self.refresh_page()

        # try:
        #     self.alert_fade()
        # except Exception:
        #     self.refresh_page()

    def click_lock(self):
        try:
            self.click(self.loc_lock_btn)
            self.confirm_tips_alert_show(self.loc_lock_btn)
        except StaleElementReferenceException:
            self.click(self.loc_lock_btn)
            self.confirm_tips_alert_show(self.loc_lock_btn)

    def click_unlock(self):
        try:
            self.click(self.loc_unlock_btn)
            self.confirm_tips_alert_show(self.loc_unlock_btn)
        except StaleElementReferenceException:
            self.click(self.loc_unlock_btn)
            self.confirm_tips_alert_show(self.loc_unlock_btn)

    def search_device_by_sn(self, sn):
        try:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            time.sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)
        except StaleElementReferenceException:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            time.sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)
        except ElementNotInteractableException:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            time.sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)

    def click_send_btn(self):
        self.click(self.loc_msg_btn)
        self.confirm_alert_existed(self.loc_msg_btn)

    def msg_input_and_send(self, msg):
        self.input_text(self.loc_msg_input_box, msg)
        self.click(self.loc_msg_input_send_btn)
        self.confirm_tips_alert_show(self.loc_msg_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_msg_btn)

    def confirm_msg_alert_fade(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_msg_input_send_btn)

    def click_devices_list_btn(self):
        self.click(self.loc_devices_list_btn)

    def click_import_btn(self):
        self.click(self.loc_import_btn)
        self.confirm_alert_existed(self.loc_import_btn)

    def click_download_template_btn(self):
        # download,
        self.click(self.loc_download_template_btn)
        # need add step check if success to download

    def import_devices_info(self, info):
        self.alert_show()
        if not os.path.exists(self.file_path):
            raise FileNotFoundError
        self.input_text(self.loc_choose_file_btn, self.file_path)
        self.select_by_text(self.loc_import_cate_btn, info['cate'])
        self.select_by_text(self.loc_import_model_btn, info['model'])
        time.sleep(3)
        self.click(self.loc_import_save_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_import_save_btn)

    def click_new_btn(self):
        self.click(self.loc_new_btn)
        self.confirm_alert_existed(self.loc_new_btn)

    def add_devices_info(self, dev_info):
        # name
        self.input_text(self.loc_input_dev_name, dev_info['name'])
        # SN
        self.input_text(self.loc_input_dev_SN, dev_info['SN'])
        # cate
        self.select_by_text(self.loc_select_dev_cate, dev_info['cate'])
        # model
        self.select_by_text(self.loc_select_dev_mode, dev_info['model'])
        # 保存
        self.click(self.loc_save_dev_btn)

    def get_add_dev_warning_alert(self):
        flag = 0
        now_time = time.time()
        while True:
            ele = self.get_element(self.loc_add_device_success_warning)
            print(ele.get_attribute("style"))
            if "block" in ele.get_attribute("style"):
                flag += 1
                break
            if time.time() > now_time + 5:
                break
            time.sleep(1)

        now_time = time.time()
        if flag == 0:
            print("运行到这里")
            while True:
                if not ("block" in self.get_element(self.loc_add_device_success_warning).get_attribute("style")):
                    self.click(self.loc_save_dev_btn)
                else:
                    break
                if time.time() > now_time + 5:
                    assert False, "无法添加device, 请检查！！！"
                time.sleep(1)

    # another alert would appear when add device successfully, would conflict
    def confirm_add_device_alert_fade_discard(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_dev_btn)

    def close_btn_add_dev_info(self):
        self.click(self.loc_close_dev_btn)
        self.alert_fade()

    # return devices_list
    def get_dev_info_list(self):
        try:
            devices_list = []
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            for tr_ele in tr_eles:
                td_eles = tr_ele.find_elements(*self.loc_td)[1:8]
                devices_list.append({"Name": td_eles[0].text, "Category": td_eles[2].text, "Model": td_eles[3].text,
                                     "SN": td_eles[4].text, "Status": td_eles[5].text,
                                     "Lock Status": td_eles[6].text})
            return devices_list
        except TimeoutException:
            return []

    # return length of devices_list
    def get_dev_info_length(self):
        try:
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            return len(tr_eles)
        except TimeoutException:
            return 0

    def select_all_devices(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_check_all))
        self.exc_js_click(ele)
        # self.deal_ele_selected(ele)
        return ele

    def select_device(self, device_sn):
        loc = (By.ID, device_sn)
        ele = self.web_driver_wait_until(EC.presence_of_element_located(loc))
        self.exc_js_click(ele)
        self.deal_ele_selected(ele)
        return ele

    def check_ele_is_selected(self, ele):
        self.deal_ele_selected(ele)

    def check_ele_is_not_selected(self, ele):
        self.deal_ele_not_selected(ele)

    def get_devices_list_label_text_discard(self):
        devices = self.get_element(self.loc_devices_list)
        label_eles = devices.find_elements(*self.loc_label)
        text = [label_ele.text for label_ele in label_eles]
        return text

    # check if alert would disappear
    def alert_fade(self):
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 10)

    # check if alert would appear
    def alert_show(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 10)

    # add single device
    def get_models_list(self):
        if self.ele_is_existed(self.loc_models_box):
            eles = self.get_elements(self.loc_models_box)
            models_list = [ele.text for ele in eles]
            # print(models_list)
            return models_list
        else:
            return []

    # get all categories
    def get_categories_list(self):
        if self.ele_is_existed(self.loc_cate_box):
            eles = self.get_elements(self.loc_cate_box)
            cates_list = [ele.text for ele in eles]
            print(cates_list)
            return cates_list
        else:
            return []

    def category_is_existed(self, cate):
        if cate in self.get_categories_list():
            return True
        else:
            return False

    # find cate element
    def find_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))

    # find model ele
    def find_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))

    # click [Create New Category] btn
    def click_category(self):
        self.click(self.loc_category_btn)
        self.confirm_alert_existed(self.loc_save_btn_cate)

    # add category
    def add_category(self, cate_name):
        self.input_text(self.loc_input_cate_box, cate_name)
        self.click(self.loc_save_btn_cate)

    def confirm_add_category_box_fade(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    # click [Create New Model] btn
    def click_model(self):
        self.click(self.loc_mode_btn)
        self.confirm_alert_existed(self.loc_mode_btn)

    # add model
    def add_model(self, model_name):
        self.input_text(self.loc_input_mode_box, model_name)
        self.click(self.loc_save_btn_mode)

    def confirm_add_model_box_fade(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    def close_btn_mode(self):
        self.click(self.loc_close_btn_mode)

    def close_btn_cate(self):
        self.click(self.loc_close_btn_cate)

    # get devices page alert text
    def get_alert_text(self):
        # 1: tip_box is existed, 2:tip_box
        # try:
        #     tips_box = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed), 5)
        #     text = tips_box.text
        #     return text
        # except TimeoutException:
        #     return False
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text

    def confirm_tips_alert_show(self, loc):
        now_time = time.time()
        while True:
            if self.get_tips_alert():
                break
            else:
                self.click(loc)
            if time.time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭，请检查！！！"

    def get_tips_alert(self):
        try:
            ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed), 5)
            print(ele.text)
            return True
        except TimeoutException:
            return False
