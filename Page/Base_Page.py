from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

class BasePage:

    def __init__(self, driver, times):
        self.driver = driver
        self.times = times

    def get_element(self, loc):
        return self.driver.find_element(*loc)

    def get_elements(self, loc):
        return self.driver.find_elements(*loc)

    def get_elements_in_range(self, loc_pre, loc_pos):
        return self.driver.find_element(*loc_pre).find_elements(*loc_pos)

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
        al = self.driver.switch_to.alert
        return al

    def alert_input_text(self, al, text):
        al.send_keys(text)

    def accept_alert(self, al):
        al.accept()

    def dismiss_alert(self, al):
        al.dismiss()

        # d = webdriver.Chrome()
        # al = d.switch_to.alert




















