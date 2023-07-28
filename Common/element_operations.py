from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


class ElementsOperations:

    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        # self.driver.maximize_window()
        # url = 'https://mdm.telpoai.com/login'
        # # 窗口最大化
        # self.driver.get(url)
        self.times = 10

    def element_find(self, loc):
        ele = self.driver.find_element(*loc)
        return ele

    def element_click(self, loc):
        self.driver.find_element(*loc).click()

    def element_clear(self, loc):
        self.driver.find_element(*loc).clear()

    def element_send_keys(self, loc, operate):
        self.driver.find_element(*loc).clear()
        self.driver.find_element(*loc).send_keys(operate)

    def element_send_keys_checkbox(self, loc, operate):
        self.driver.find_element(*loc).send_keys(operate)

    def web_driver_wait_until(self, condition, times=0):
        if times == 0:
            wait_times = self.times
        else:
            wait_times = times
        return WebDriverWait(self.driver, wait_times).until(condition)

    def web_driver_wait_until_not(self, condition,  times=0):
        if times == 0:
            wait_times = self.times
        else:
            wait_times = times
        return WebDriverWait(self.driver, wait_times).until_not(condition)

# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(30)
#     driver.maximize_window()
#     url = 'https://mdm.telpoai.com/login'
#     # 窗口最大化
#     driver.get(url)
#
#     case = ElementsOperations(driver)
#     loc_agree = (By.XPATH, "//*[@id=\"agreeTerms\"]")
#     case.wait_presence_of_element_located(loc_agree)
#     case.element_send_keys_checkbox(loc_agree, Keys.SPACE)
#     time.sleep(10)
