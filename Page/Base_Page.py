from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage:

    def __init__(self, driver, times):
        self.driver = driver
        self.times = times

    def quit_browser(self):
        self.driver.quit()

    def confirm_alert_not_existed(self, loc, ex_js=0):
        print("====到这里来了")
        while True:
            if self.alert_is_not_existed():
                break
            else:
                print("====else 里面")
                # self.click(release_btn)
            if ex_js == 1:
                if self.alert_is_not_existed():
                    break
                self.exc_js_click_loc(loc)
            else:
                self.click(loc)
                print("已经点击了")
            if time.time() > self.return_end_time():
                assert False, "@@@@弹窗无法关闭 出错， 请检查！！！"

    def confirm_alert_existed(self, loc, ex_js=0):
        while True:
            if self.alert_is_existed():
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
            time.sleep(1)
            if time.time() > self.return_end_time():
                assert False, "@@@@弹窗无法打开 出错， 请检查！！！"

    def alert_is_existed(self):
        if EC.alert_is_present():
            return True
        else:
            return False

    def alert_is_not_existed(self):
        if EC.alert_is_present():
            return False
        else:
            return True

    def ele_is_existed(self, loc):
        try:
            self.driver.find_element(*loc)
            return True
        except Exception:
            return False

    def return_end_time(self):
        timeout = 180
        timedelta = 1
        end_time = time.time() + timeout
        return end_time

    def move_and_click(self, ele):
        ActionChains(self.driver).move_to_element(ele).click().perform()

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(1)

    def get_selector(self, loc):
        ele = self.get_element(loc)
        select = Select(ele)
        return select

    def exc_js_click(self, ele):
        self.driver.execute_script("arguments[0].click();", ele)

    def exc_js_click_loc(self, loc):
        ele = self.get_element(loc)
        self.driver.execute_script("arguments[0].click();", ele)

    def deal_ele_selected(self, ele):
        while True:
            if self.ele_is_selected(ele):
                break
            else:
                self.exc_js_click(ele)
            time.sleep(1)
            if time.time() > self.return_end_time():
                assert False, "@@@无法选中check box, 请检查！！！"

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

    def check_ele_is_selected(self, ele):
        if not self.ele_is_selected(ele):
            self.web_driver_wait_until(EC.element_to_be_selected(ele))

    def check_ele_is_not_selected(self, ele):
        if self.ele_is_selected(ele):
            self.web_driver_wait_until_not(EC.element_to_be_selected(ele))

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
