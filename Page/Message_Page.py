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
    loc_js_link = (By.CLASS_NAME, "nav-link")
    loc_li_sn = (By.TAG_NAME, "li")

    # messages list relate
    loc_message_box = (By.CLASS_NAME, "message")
    loc_message_text = (By.CLASS_NAME, "text")
    loc_message_status = (By.CSS_SELECTOR, "[class = 'status text-danger']")

    def choose_device(self, sn, cate):
        device_list = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_device_list))
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_li_sn))
        # devices_sn = device_list.find_elements(*self.loc_li_sn)
        # check if device is dispalyed
        while True:
            # if sn in res, ele is displayed
            res = [dev.get_attribute("data-sn") for dev in device_list.find_elements(*self.loc_li_sn)]
            if sn not in res:
                self.drop_down_categories(cate)
                time.sleep(1)
            else:
                break

        for device in device_list.find_elements(*self.loc_li_sn):
            if sn == device.get_attribute("data-sn"):
                self.exc_js_click(device)

    def drop_down_categories(self, cate):
        device_list = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_device_list))
        eles = device_list.find_elements(*self.loc_cate_tag_name)
        for ele in eles:
            if cate in ele.text:
                print(ele.text)
                # ele.click()
                self.exc_js_click(ele)
                break

    def click_related_device_discard(self, sn):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_drop_down_menu_open))
        eles = self.get_element(self.loc_drop_down_menu_open).find_elements(*self.loc_device_sn)
        for ele in eles:
            if sn in ele.text:
                ele.click()
        flag = 0
        for i in range(5):
            if self.get_element(self.loc_drop_down_menu_open).find_element(*self.loc_device_active):
                flag += 1
                break
            time.sleep(1)
        if flag == 0:
            assert False, "@@@@展开menu失败！！！， 请检查！！！"

    def get_device_message_list(self, length):
        self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_message_box))
        message_boxes = self.get_elements(self.loc_message_box)[:length]
        print(message_boxes)
        print(len(message_boxes))
        message_list = []
        for box in message_boxes:
            msg_text = box.find_element(*self.loc_message_text).text
            msg_status = box.find_element(*self.loc_message_status).text
            message = {"message": msg_text, "status": msg_status}
            message_list.append(message)
        return message_list
