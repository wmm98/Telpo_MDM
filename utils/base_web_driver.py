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
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        url = 'https://mdm.telpoai.com/login'
        # 窗口最大化
        self.driver.get(url)


if __name__ == '__main__':
    BaseWeb()
