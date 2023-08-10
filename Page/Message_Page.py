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
    loc_cate_tag_name = (By.TAG_NAME, "p")
    # count the opens and check if all drop down open really
    loc_drop_down_menu_open = (By.CSS_SELECTOR, "[class = 'nav-item menu-open']")
    loc_device_sn = (By.CLASS_NAME, "small")
    loc_device_active = (By.CLASS_NAME, "active")

    # messages list relate
    loc_message_box = (By.CLASS_NAME, "message")
    loc_message_text = (By.CLASS_NAME, "text")
    loc_message_status = (By.CSS_SELECTOR, "status text-danger")

    def get_device_message_dict(self, length):
        self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_message_box))
        message_boxes = self.get_elements(self.loc_message_box)[length]
        message_list = []
        for box in message_boxes:
            msg_text = box.find_element(*self.loc_message_text)
            msg_status = box.find_element(*self.loc_message_status)
            message = {"message": msg_text, "status": msg_status}
            message_list.append(message)


    def close_menu(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_drop_down_menu_open))
        ele = self.get_element(self.loc_drop_down_menu_open).find_element(*self.loc_cate_tag_name)
        ele.click()
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_drop_down_menu_open))

    def drop_down_categories(self, cate):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_device_list))
        self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_cate_tag_name))
        eles = self.get_elements(self.loc_cate_tag_name)
        for ele in eles:
            if cate in ele.text:
                ele.click()
                break

    def click_related_device(self, sn):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_drop_down_menu_open))
        eles = self.get_element(self.loc_drop_down_menu_open).find_elements(*self.loc_device_sn)
        for ele in eles:
            if sn in ele.text:
                print(ele.text)
                ele.click()
        # try:
        #     if self.get_element(self.loc_drop_down_menu_open).find_element(*self.loc_device_active):
        #         pass
        # except Exception as e:
        #     print("@@@@检查active！！！")
        #     print(e)
