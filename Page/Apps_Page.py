from selenium.common import TimeoutException
from Conf.Config import Config
from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time

conf = Config()


class APPSPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    # private app related
    loc_private_app_btn = (By.LINK_TEXT, "Private Apps")
    private_app_main_title = "Private Apps"

    # search relate
    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_search_app_name = (By.ID, "search_app_name")
    loc_search_search = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_search_app_button']")

    # new apk btn
    loc_new_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square']")
    loc_choose_file = (By.ID, "file")
    loc_choose_category = (By.ID, "Category")
    loc_developer_box = (By.ID, "developer")
    loc_des_box = (By.ID, "desc")
    loc_apk_save_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_create_app_button']")

    # alert show
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")

    # app list relate
    loc_apps_list = (By.ID, "apps_list")
    loc_single_app_box = (
        By.CSS_SELECTOR, "[class = 'col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column']")
    # app delete btn
    loc_app_delete_btn = (By.CSS_SELECTOR, "[class = 'btn btn-sm bg-danger']")
    loc_app_confirm_del_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-light deleteapp_button']")
    # app release btn
    loc_app_release_btn = (By.CSS_SELECTOR, "[class = 'fas fa-registered']")
    loc_app_release_alert = (By.ID, "modal-app-release")
    loc_silent_install = (By.ID, "setsilent")
    loc_device_selected_box = (By.CLASS_NAME, "label-selected")
    loc_device_list = (By.CLASS_NAME, "label-item")
    loc_single_device = (By.TAG_NAME, "span")
    loc_app_package_name = (By.ID, "release_apk_package")
    loc_app_release_confirm = (By.CSS_SELECTOR, "[class = 'btn btn-primary confirm_release']")

    def click_release_app_btn(self):
        self.click(self.loc_app_release_btn)
        self.confirm_alert_existed(self.loc_app_release_btn)

    def get_app_package_name(self):
        name = self.get_element(self.loc_app_package_name).text
        return name

    def input_release_app_info(self, info):
        self.select_by_text(self.loc_silent_install, info["silent"])
        time.sleep(3)
        devices = self.get_element(self.loc_device_list).find_elements(*self.loc_single_device)
        selected_text = self.get_element(self.loc_device_selected_box).text
        for device in devices:
            if info["sn"] in device.text:
                if info["sn"] in selected_text:
                    break
                while True:
                    if info["sn"] in selected_text:
                        break
                    else:
                        device.click()
                        print("运行到这里")
                    if time.time() > self.return_end_time():
                        assert False, "@@@无法选中device sn, 请检查！！！"
                    time.sleep(1)
        time.sleep(5)
        self.click(self.loc_app_release_confirm)
        self.confirm_alert_not_existed(self.loc_app_release_confirm)

    def click_delete_app_btn(self):
        self.click(self.loc_app_delete_btn)
        self.confirm_alert_existed(self.loc_app_delete_btn)
        self.click(self.loc_app_confirm_del_btn)
        self.confirm_alert_not_existed(self.loc_app_confirm_del_btn)

    def get_apps_text_list(self):
        if self.ele_is_existed(self.loc_single_app_box):
            boxes = self.get_elements(self.loc_single_app_box)
            return [box.text for box in boxes]
        else:
            return []

    def search_app_by_name(self, app_name):
        self.click(self.loc_search_btn)
        self.confirm_alert_existed(self.loc_search_btn)
        self.input_text(self.loc_search_app_name, app_name)
        time.sleep(1)
        self.click(self.loc_search_search)
        self.confirm_alert_not_existed(self.loc_search_search)

    def click_private_app_btn(self):
        self.click(self.loc_private_app_btn)
        while True:
            if self.private_app_main_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_private_app_btn)
            if time.time() > self.return_end_time():
                assert False, "@@@@打开private app page 出错！！！"

    def click_add_btn(self):
        self.click(self.loc_new_btn)
        self.confirm_alert_existed(self.loc_new_btn)

    def input_app_info(self, info):
        self.input_text(self.loc_choose_file, info["file_name"])
        self.select_by_text(self.loc_choose_category, info["file_category"])
        self.input_text(self.loc_developer_box, info["developer"])
        self.input_text(self.loc_des_box, info["description"])
        time.sleep(1)
        self.click(self.loc_apk_save_btn)
        # self.confirm_alert_not_existed(self.loc_apk_save_btn)

    # def click_save_add_app(self):
    #     ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_apk_save_btn))
    #     self.exc_js_click_loc(self.loc_apk_save_btn)

    def check_add_app_save_btn(self):
        self.confirm_alert_not_existed(self.loc_apk_save_btn)

    def alert_fade(self):
        try:
            self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 10)
            return True
        except TimeoutException:
            return False

        # check if alert would appear

    def alert_show(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 10)
            return True
        except TimeoutException:
            return False

    def get_alert_text(self):
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text

    def confirm_alert_not_existed(self, loc, ex_js=0):
        while True:
            if self.alert_fade():
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
