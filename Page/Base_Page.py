from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.times = 10

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

    def web_driver_wait_until(self, condition, times=0):
        if times == 0:
            wait_times = self.times
        else:
            wait_times = times
        return WebDriverWait(self.driver, wait_times).until(condition)

    def web_driver_wait_until_not(self, condition, times=0):
        if times == 0:
            wait_times = self.times
        else:
            wait_times = times
        return WebDriverWait(self.driver, wait_times).until_not(condition)




















