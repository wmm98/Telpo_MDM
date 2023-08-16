from selenium.common import TimeoutException
from Conf.Config import Config
from Page.Telpo_MDM_Page import TelpoMDMPage
# from Page.System_Page import SystemPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time

conf = Config()


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

    # add OTA package btn relate
    loc_add_package_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square']")
    loc_choose_package_btn = (By.ID, "customFile")
    loc_file_category = (By.ID, "cid")
    loc_android_checkbox = (By.ID, "customRadio1")
    loc_linux_checkbox = (By.ID, "customRadio2")
    loc_save_package_info_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-submit']")

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
    loc_sn_text = (By.TAG_NAME, "span")
    loc_label_selected = (By.CLASS_NAME, "label-selected")

    loc_ota_list = (By.ID, "otalist")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")

    # package release module relate
    loc_package_releases_btn = (By.LINK_TEXT, "Package Releases")
    ota_release_package_title = "OTA Package Releases"
    loc_data_body = (By.ID, "databody")
    loc_single_log = (By.TAG_NAME, "tr")
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

    def click_package_release_page(self):
        self.click(self.loc_package_releases_btn)
        while True:
            if self.ota_release_package_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_package_releases_btn)
            if time.time() > self.return_end_time():
                assert False, "@@@@ 打开package release 出错！！！"

    def get_release_log_length(self):
        body_list = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_data_body))
        if "No Data" in body_list.text:
            return 0

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
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_release_search_btn))
        self.click(self.loc_release_search_btn)
        self.confirm_alert_existed(self.loc_release_search_btn)
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_release_package_name))
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_release_sn))
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_release_search))
        self.input_text(self.loc_search_release_package_name, info["package_name"])
        self.input_text(self.loc_search_release_sn, info["sn"])
        time.sleep(1)
        self.click(self.loc_search_release_search)
        self.confirm_alert_not_existed(self.loc_search_release_search)

        if count:
            if "NO Data" in self.get_element(self.loc_data_body).text:
                assert False, "@@@@找不到此包 %s %s 的release 记录, 请检查！！！" % (info["package_name"], info["sn"])

            # boxes = self.get_elements(self.loc_packages_box)
            # if len(boxes) != 1:
            #     assert False, "@@@@有多个相同的  %s %s 释放记录, 请检查！！！" % (info["package_name"], info["sn"])

    def release_again(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_send_release_again_btn))
        self.click(self.loc_send_release_again_btn)

    # def
    #     text = self.get_alert_text()
    #     if not (exp_text in text):
    #         self.click(self.loc_send_release_again_btn)

    def delete_all_release_log(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_release_check_all))
        # print(ele)
        self.exc_js_click_loc(self.loc_release_check_all)
        self.deal_ele_selected(ele)
        self.click(self.loc_release_delete_btn)
        self.confirm_alert_existed(self.loc_release_delete_btn)
        self.click(self.loc_release_confirm_del)
        self.confirm_alert_not_existed(self.loc_release_confirm_del)
        # self.refresh_page()
        while True:
            if self.get_release_log_length() == 0:
                break
            else:
                self.exc_js_click_loc(self.loc_release_check_all)
                self.deal_ele_selected(ele)
                self.click(self.loc_release_delete_btn)
                self.confirm_alert_existed(self.loc_release_delete_btn)
            time.sleep(1)
            if time.time() > self.return_end_time():
                assert False, "@@@@删除全部release ota logs 出错, 请检查！！！"

    def select_release_log(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_log_check_box))
        self.exc_js_click_loc(self.loc_log_check_box)
        self.deal_ele_selected(ele)

    def click_upgrade_packages(self):
        self.click(self.loc_upgrade_packages_btn)
        while True:
            if self.upgrade_package_main_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_upgrade_packages_btn)
            if time.time() > self.return_end_time():
                assert False, "@@@@ 打开upgrade packages 出错！！！"

    def get_package_ele_discard(self, pack_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_packages_box))
        eles = self.get_elements(self.loc_packages_box)
        for ele in eles:
            if pack_name in ele.text:
                return ele

    def click_release_btn(self):
        self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_release_btn))
        self.click(self.loc_release_btn)
        try:
            self.alert_show()
        except TimeoutException:
            self.confirm_alert_existed(self.loc_release_btn)

    def input_release_OTA_package(self, release_info):
        # {"network": "NO Limit", "silent": 0, "category": "No Limit"}
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_download_network))
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
                # self.click(ele_sn)
                ele_sn.click()
                print("选中的text: ", self.get_element(self.loc_label_selected).text)
                break
        time.sleep(3)

    def click_alert_release_btn(self):
        # self.click(self.loc_release_package_btn)
        # print("弹窗是否存在：", self.alert_is_existed())
        try:
            self.exc_js_click(self.get_element(self.loc_release_package_btn))
            text = self.get_alert_text()
            return text
        except Exception:
            self.confirm_alert_not_existed(self.loc_release_package_btn, ex_js=1)

    def search_device_by_pack_name(self, pack_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_btn))
        self.click(self.loc_search_btn)
        self.alert_show()
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_search_package))
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_category))
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_search_search_btn))
        self.input_text(self.loc_input_search_package, pack_name)
        time.sleep(1)
        self.click(self.loc_search_search_btn)
        self.confirm_alert_not_existed(self.loc_search_search_btn)
        if "NO Data" in self.get_element(self.loc_ota_list).text:
            assert False, "@@@@找不到此包 %s, 请检查！！！" % pack_name

        boxes = self.get_elements(self.loc_packages_box)
        if len(boxes) != 1:
            assert False, "@@@@有多个相同的包 %s, 请检查！！！" % pack_name

        try:
            self.alert_fade()
        except Exception:
            self.click(self.loc_search_search_btn)
            self.alert_fade()

    def click_add_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_add_package_btn))
        self.click(self.loc_add_package_btn)
        self.confirm_alert_existed(self.loc_add_package_btn)

    def input_ota_package_info(self, info):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_choose_package_btn))
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
        time.sleep(5)

    def click_save_add_ota_pack(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_save_package_info_btn))
        self.click(self.loc_save_package_info_btn)

    # check if alert would disappear
    def alert_fade(self):
        try:
            self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 6)
            return True
        except TimeoutException:
            return False

    # check if alert would appear
    def alert_show(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 6)
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
