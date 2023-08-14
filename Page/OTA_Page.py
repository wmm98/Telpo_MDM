from selenium.common import TimeoutException
from Conf.Config import Config
from Page.Telpo_MDM_Page import TelpoMDMPage
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

    # search alert
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade modal_dark show']")

    # package box relate
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

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")

    # package release relate
    loc_data_body = (By.ID, "databody")

    def get_release_log_length(self):
        body_list = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_data_body))
        if "No Data" in body_list.text:
            return 0

    def check_single_release_info(self):
        if self.get_release_log_length() == 0:
            assert False, "@@@@没有OTA release的记录， 请检查！！！"



    def click_upgrade_packages(self):
        self.click(self.loc_upgrade_packages_btn)
        while True:
            if self.upgrade_package_main_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_upgrade_packages_btn)
            if time.time() > self.return_end_time():
                assert False, "@@@@ 打开upgrade packages 出错！！！"

    def get_package_ele(self, pack_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_packages_box))
        eles = self.get_elements(self.loc_packages_box)
        for ele in eles:
            if pack_name in ele.text:
                return ele

    def click_release_btn(self, ele):
        self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_release_btn))
        release_btn = ele.find_element(*self.loc_release_btn)
        release_btn.click()
        # self.click(release_btn)
        try:
            self.alert_show()
        except TimeoutException:
            while True:
                if self.alert_is_existed():
                    break
                else:
                    # self.click(release_btn)
                    release_btn.click()
                time.sleep(1)
                if time.time() > self.return_end_time():
                    assert False, "@@@@Release OTA Package 出错， 请检查！！！"

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
        self.exc_js_click(self.get_element(self.loc_release_package_btn))

        time.sleep(3)

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
        time.sleep(1)
        # ele_search = self.get_element(self.loc_search_search_btn)
        # self.exc_js_click(ele_search)
        try:
            self.alert_fade()
        except Exception:
            self.click(self.loc_search_search_btn)
            self.alert_fade()

    # check if alert would disappear
    def alert_fade(self):
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 6)

    # check if alert would appear
    def alert_show(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 6)

    def get_alert_text(self):
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text
