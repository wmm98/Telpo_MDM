from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Page.Base_Page import BasePage


class TelpoMDMPage(BasePage):
    def __init__(self, driver, times):
        BasePage.__init__(self, driver, times)

    # loc_devics_map_btn =
    # loc_apps_btn =
    loc_main_title = (By.CLASS_NAME, "m-0")
    loc_devices_page_btn = (By.XPATH, "/html/body/div[1]/aside[1]/div/div[4]/div/div/nav/ul/li[2]")

    def get_loc_main_title(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_main_title))
        main_title = self.get_element(self.loc_main_title)
        act_main_title = main_title.text
        return act_main_title

    def click_devices_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_devices_page_btn))
        self.click(self.loc_devices_page_btn)

    def click_apps_btn(self):
        pass
















