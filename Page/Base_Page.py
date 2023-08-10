from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


class BasePage:

    def __init__(self, driver, times):
        self.driver = driver
        self.times = times

    # def stop_page(self):
    #     self.driver.

    def move_and_click(self, ele):
        ActionChains(self.driver).move_to_element(ele).click().perform()

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

    def web_driver_wait_until(self, condition, wait_times=0):
        if wait_times == 0:
            return WebDriverWait(self.driver, self.times).until(condition)
        else:
            return WebDriverWait(self.driver, wait_times).until(condition)

    def web_driver_wait_until_not(self, condition, wait_times=0):
        if wait_times == 0:
            return WebDriverWait(self.driver, self.times).until_not(condition)
        else:
            return WebDriverWait(self.driver, wait_times).until_not(condition)

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
