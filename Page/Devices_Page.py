from selenium.common import TimeoutException
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
    loc_msg_input_close_btn_large = (By.ID, "modal-device-message")   # just for serach the exact close btn
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

    def click_reboot_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_lock_btn))
        self.click(self.loc_lock_btn)

    def click_lock(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_lock_btn))
        self.click(self.loc_lock_btn)

    def click_unlock(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_unlock_btn))
        self.click(self.loc_unlock_btn)

    def search_device_by_sn(self, sn):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_btn))
        self.click(self.loc_search_btn)
        self.alert_show()
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_input_box))
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_search_btn))
        self.input_text(self.loc_search_input_box, sn)
        time.sleep(1)
        self.click(self.loc_search_search_btn)
        time.sleep(1)
        # ele_search = self.get_element(self.loc_search_search_btn)
        # self.exc_js_click(ele_search)
        try:
            self.alert_fade()
        except Exception:
            self.click(self.loc_search_search_btn)
            self.alert_fade()

    def click_send_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_msg_btn))
        self.click(self.loc_msg_btn)

    def msg_input_and_send(self, msg):
        self.alert_show()
        self.input_text(self.loc_msg_input_box, msg)
        self.click(self.loc_msg_input_send_btn)

    def click_devices_list_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located((self.loc_devices_list_btn)))
        self.click(self.loc_devices_list_btn)

    def click_import_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_import_btn))
        self.click(self.loc_import_btn)

    def click_download_template_btn(self):
        self.alert_show()
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

    def click_new_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_new_btn))
        self.click(self.loc_new_btn)
        self.alert_show()

    def add_devices_info(self, dev_info):
        # name
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_dev_name))
        self.input_text(self.loc_input_dev_name, dev_info['name'])
        # SN
        self.input_text(self.loc_input_dev_SN, dev_info['SN'])
        # cate
        self.select_by_text(self.loc_select_dev_cate, dev_info['cate'])
        # model
        self.select_by_text(self.loc_select_dev_mode, dev_info['model'])
        # 保存
        self.click(self.loc_save_dev_btn)

    def close_btn_add_dev_info(self):
        self.click(self.loc_close_dev_btn)
        self.alert_fade()

    # return devices_list
    def get_dev_info_list(self):
        try:
            devices_list = []
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_devices_list))
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            for tr_ele in tr_eles:
                td_eles = tr_ele.find_elements(*self.loc_td)[1:8]
                devices_list.append({"Name": td_eles[0].text, "SN": td_eles[4].text, "Status": td_eles[5].text,
                                     "Lock Status": td_eles[6].text})
            return devices_list
        except TimeoutException:
            return []

    # return length of devices_list
    def get_dev_info_length(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_devices_list))
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            return len(tr_eles)
        except TimeoutException:
            return 0

    def select_all_devices(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_check_all))
        self.exc_js_click(ele)
        return ele

    def select_device(self, device_sn):
        loc = (By.ID, device_sn)
        ele = self.web_driver_wait_until(EC.presence_of_element_located(loc))
        self.exc_js_click(ele)
        return ele

    def check_ele_is_selected(self, ele):
        if not self.ele_is_selected(ele):
            self.web_driver_wait_until(EC.element_to_be_selected(ele))

    def check_ele_is_not_selected(self, ele):
        if self.ele_is_selected(ele):
            self.web_driver_wait_until_not(EC.element_to_be_selected(ele))

    def get_devices_list_label_text_discard(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_devices_list))
        devices = self.get_element(self.loc_devices_list)
        label_eles = devices.find_elements(*self.loc_label)
        text = [label_ele.text for label_ele in label_eles]
        return text

    # check if alert would disappear
    def alert_fade(self):
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show))

    # check if alert would appear
    def alert_show(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show))

    # add single device
    def get_models_list(self):
        try:
            self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_models_box))
            eles = self.get_elements(self.loc_models_box)
            models_list = [ele.text for ele in eles]
            print(models_list)
            return models_list
        except TimeoutException:
            return []

    # get all categories
    def get_categories_list(self):
        try:
            self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_cate_box))
            eles = self.get_elements(self.loc_cate_box)
            cates_list = [ele.text for ele in eles]
            print(cates_list)
            return cates_list
        except TimeoutException:
            return []

    # find cate element
    def find_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))

    # find model ele
    def find_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))

    # click [Create New Category] btn
    def click_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))
        self.click(self.loc_category_btn)

    # add category
    def add_category(self, cate_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_cate_box))
        self.input_text(self.loc_input_cate_box, cate_name)
        self.click(self.loc_save_btn_cate)

    # click [Create New Model] btn
    def click_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))
        self.click(self.loc_mode_btn)

    # add model
    def add_model(self, model_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_mode_box))
        self.input_text(self.loc_input_mode_box, model_name)
        self.click(self.loc_save_btn_mode)

    def close_btn_mode(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_close_btn_mode))
        self.click(self.loc_close_btn_mode)

    def close_btn_cate(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_close_btn_cate))
        self.click(self.loc_close_btn_cate)

    # get devices page alert text
    def get_alert_text(self):
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text

