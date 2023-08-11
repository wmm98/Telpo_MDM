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

    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_input_search_package = (By.ID, "searchname")
    loc_search_category = (By.ID, "searchcate")
    loc_search_search_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-search']")

    # search alert
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade modal_dark show']")

    def search_device_by_sn(self, pack_name):
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
