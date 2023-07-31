from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver



class BasePage:

    def __init__(self, driver, times):
        self.driver = driver
        self.times = times

    def get_element(self, loc):
        return self.driver.find_element(*loc)

    def input_text(self, loc, text):
        ele = self.get_element(loc)
        ele.clear()
        ele.send_keys(text)

    def input_keyboard(self, loc, keyboard):
        ele = self.get_element(loc)
        ele.send_keys(keyboard)

    def click(self, loc):
        self.driver.find_element(*loc).click()

    def get_title(self):
        return self.driver.title

    def web_driver_wait_until(self, condition):
        return WebDriverWait(self.driver, self.times).until(condition)

    def web_driver_wait_until_not(self, condition):
        return WebDriverWait(self.driver, self.times).until_not(condition)

    def switch_to_alert(self):
        alert = self.driver.switch_to.alert

        # d = webdriver.Chrome()
        # al = d.switch_to.alert




















