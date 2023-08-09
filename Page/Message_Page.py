from selenium.common import TimeoutException
from Conf.Config import Config
from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time


class MessagePage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_device_list = (By.CLASS_NAME, "devicelist")
    loc_devices = (By.CLASS_NAME, "small")
    loc_drop_down_btns = (By.CSS_SELECTOR, "[class = 'right fas fa-angle-left']")
    # count the opens and check if all drop down open really
    loc_drop_down_menu_open = (By.CSS_SELECTOR, "[class = 'nav-item menu-open']")

    def get_devices_sn_list(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_device_list))

    def length_drop_down_categories(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_device_list))
        eles = self.get_elements(self.loc_drop_down_btns)
        for ele in eles:
            ele.click()
        time.sleep(1)
        return len(eles)

    def length_menus_open(self):
        menus_opens = self.get_elements(self.loc_drop_down_menu_open)
        return len(menus_opens)

    def check_categories_drop_down(self):
        for i in range(5):
            if self.length_drop_down_categories() == self.length_menus_open():
                break
            self.refresh_page()











