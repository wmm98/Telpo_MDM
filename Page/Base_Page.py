from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.select import Select


class BasePage:

    def __init__(self, driver, times):
        self.driver = driver
        self.times = times

    def refresh_page(self):
        self.driver.refresh()

    def get_selector(self, loc):
        ele = self.get_element(loc)
        select = Select(ele)
        return select

    def exc_js_click(self, ele):
        self.driver.execute_script("arguments[0].click();", ele)

    def ele_is_selected(self, ele):
        return ele.is_selected()

    def select_by_text(self, loc, value):
        select = self.get_selector(loc)
        # select.select_by_value(value)
        select.select_by_visible_text(value)

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
