import Page as public_pack
from Page.Base_Page import BasePage

By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time
test_yml = public_pack.yaml_data


class TelpoMDMPage(BasePage):
    def __init__(self, driver, times):
        BasePage.__init__(self, driver, times)

    # loc_devics_map_btn =
    # loc_apps_btn =
    loc_main_title = (By.CLASS_NAME, "m-0")
    loc_devices_page_btn = (By.XPATH, "/html/body/div[1]/aside[1]/div/div[4]/div/div/nav/ul/li[2]")

    loc_message_page_btn = (By.CSS_SELECTOR, "[class = 'nav-icon fas fa-envelope']")

    loc_OTA_btn = (By.LINK_TEXT, "OTA")
    loc_OTA_menu_open = (By.CSS_SELECTOR, "[class = 'nav-item menu-is-opening menu-open']")

    loc_Apps_btn = (By.LINK_TEXT, "Apps")
    loc_Apps_menu_open = (By.CSS_SELECTOR, "[class = 'nav-item menu-is-opening menu-open']")

    loc_system_btn = (By.LINK_TEXT, "System")

    def get_loc_main_title(self):
        main_title = self.get_element(self.loc_main_title)
        act_main_title = main_title.text
        return act_main_title

    def click_devices_btn(self):
        self.click(self.loc_devices_page_btn)

    def click_message_btn(self):
        self.click(self.loc_message_page_btn)

    def click_OTA_btn(self):
        # self.refresh_page()
        # if not self.ele_is_existed(self.loc_OTA_menu_open):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_OTA_btn))
        self.click(self.loc_OTA_btn)
        # while True:
        #     if self.ele_is_existed(self.loc_OTA_menu_open):
        #         break
        #     else:
        #         self.click(self.loc_OTA_btn)
        #     if time.time() > self.return_end_time():
        #         assert False, "@@@@OTA页面打开出错！！！！"
        #     time.sleep(1)

    def click_apps_btn(self):
        # self.refresh_page()
        # if not self.ele_is_existed(self.loc_Apps_menu_open):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_Apps_btn))
        self.click(self.loc_Apps_btn)
        # while True:
        #     if self.ele_is_existed(self.loc_Apps_menu_open):
        #         break
        #     else:
        #         self.click(self.loc_Apps_btn)
        #     if time.time() > self.return_end_time():
        #         assert False, "@@@@Apps页面打开出错！！！！"
        #     time.sleep(1)

    def click_system_btn(self):
        # self.refresh_page()
        # if not self.ele_is_existed(self.loc_Apps_menu_open):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_system_btn))
        self.click(self.loc_system_btn)
        # while True:
        #     if self.ele_is_existed(self.loc_Apps_menu_open):
        #         break
        #     else:
        #         self.click(self.loc_system_btn)
        #     if time.time() > self.return_end_time():
        #         assert False, "@@@@Apps页面打开出错！！！！"
        #     time.sleep(1)

    def deal_main_title(self, loc, title):
        now_time = self.get_current_time()
        while True:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_main_title))
            if not (title in self.get_loc_main_title()):
                self.click(loc)
            else:
                break
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@加载页面失败！！！"
            self.time_sleep(1)

    def go_to_new_address(self, url):
        address = "%s/%s" % (test_yml["website_info"]["test_base_url"], url)
        self.driver.get(address)
        now_time = self.get_current_time()
        if self.driver.current_url != address:
            while True:
                if self.driver.current_url == address:
                    break
                else:
                    self.driver.get(address)
                if self.get_current_time() > self.return_end_time(now_time):
                    assert False, "@@@打开 %s 失败， 请检查！！！" % address
                self.time_sleep(1)
        self.page_load_complete()
