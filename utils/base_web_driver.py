import time
import allure
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common.element_operations import ElementsOperations
import pytest


class BaseWeb:

    def __init__(self):
        pass

    def open_web_site(self):
        global driver
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.maximize_window()
        url = 'https://mdm.telpoai.com/login'
        # 窗口最大化
        driver.get(url)

    def get_web_driver(self):
        return driver


if __name__ == '__main__':
    case = BaseWeb()
    case.open_web_site()
    case.get_web_driver()
