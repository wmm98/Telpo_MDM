from datetime import datetime
import re
from selenium.common import TimeoutException
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

    def comm_alert_fade(self, loc):
        try:
            self.web_driver_wait_until_not(EC.presence_of_element_located(loc), 5)
            return True
        except TimeoutException:
            return False

    def comm_alert_show(self, loc):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(loc), 5)
            return True
        except TimeoutException:
            return False

    def comm_confirm_alert_not_existed(self, alert_loc, ele_loc, ex_js=0):
        now_time = time.time()
        while True:
            if self.comm_alert_fade(alert_loc):
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(ele_loc)
                else:
                    self.click(ele_loc)
            if time.time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭 出错， 请检查！！！"
            time.sleep(1)

    def confirm_alert_not_existed(self, loc, ex_js=0):
        now_time = time.time()
        while True:
            if self.alert_is_not_existed():
                break
            else:
                if ex_js == 1:
                    if self.alert_is_not_existed():
                        break
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
                if time.time() > self.return_end_time(now_time):
                    assert False, "@@@@弹窗无法关闭 出错， 请检查！！！"

    def confirm_alert_existed(self, loc, ex_js=0):
        now_time = time.time()
        while True:
            if self.alert_is_existed():
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
            time.sleep(1)
            if time.time() > self.return_end_time(now_time):
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
            self.get_element(loc)
            return True
        except Exception:
            return False

    def ele_is_existed_in_range(self, range_loc, loc):
        try:
            self.get_element(range_loc).find_elements(*loc)
            return True
        except Exception:
            return False

    def page_is_loaded(self):
        if self.driver.execute_script('return document.readyState;') == 'complete':
            return True
        else:
            return False

    def page_load_complete(self):
        now_time = time.time()
        while True:
            if self.page_is_loaded():
                print("网页完全加载完成")
                break
            print("网页还没有加载完成")
            time.sleep(1)
            if now_time > self.return_end_time(now_time, 60):
                self.refresh_page()
                break

    def return_end_time(self, now_time, timeout=180):
        timedelta = 1
        end_time = now_time + timeout
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
        self.web_driver_wait_until(EC.presence_of_element_located(loc))
        ele = self.get_element(loc)
        self.driver.execute_script("arguments[0].click();", ele)

    def deal_ele_selected(self, ele):
        now_time = time.time()
        while True:
            if self.ele_is_selected(ele):
                break
            else:
                self.exc_js_click(ele)
            time.sleep(1)
            if time.time() > self.return_end_time(now_time):
                assert False, "@@@无法选中check box, 请检查！！！"

    def deal_ele_not_selected(self, ele):
        now_time = time.time()
        while True:
            if not self.ele_is_selected(ele):
                break
            else:
                self.exc_js_click(ele)
            time.sleep(1)
            if time.time() > self.return_end_time(now_time):
                assert False, "@@@无法选中check box, 请检查！！！"

    def ele_is_selected(self, ele):
        return ele.is_selected()

    def select_by_text(self, loc, value):
        self.web_driver_wait_until(EC.presence_of_element_located(loc))
        select = self.get_selector(loc)
        # select.select_by_value(value)
        select.select_by_visible_text(value)

    def get_element(self, loc):
        self.web_driver_wait_until(EC.presence_of_element_located(loc))
        return self.driver.find_element(*loc)

    def get_elements(self, loc):
        self.web_driver_wait_until(EC.presence_of_all_elements_located(loc))
        return self.driver.find_elements(*loc)

    def get_elements_in_range(self, loc_pre, loc_pos):
        return self.driver.find_element(*loc_pre).find_elements(*loc_pos)

    def input_text(self, loc, text):
        self.web_driver_wait_until(EC.presence_of_element_located(loc))
        ele = self.get_element(loc)
        ele.clear()
        ele.send_keys(text)

    def input_keyboard(self, loc, keyboard):
        self.web_driver_wait_until(EC.presence_of_element_located(loc))
        ele = self.get_element(loc)
        ele.send_keys(keyboard)

    def click(self, loc):
        self.web_driver_wait_until(EC.presence_of_element_located(loc))
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

    def extract_integers(self, text):
        pattern = r"\d+"
        integers = re.findall(pattern, text)
        if len(integers) != 0:
            return [int(inter) for inter in integers]
        else:
            return integers

    def format_string_time(self, time_list):
        format_time = "%d-%d-%d %d:%d" % (time_list[2], time_list[0], time_list[1], time_list[3], time_list[4])
        return format_time

    def compare_time(self, time1, time2):
        dt1 = datetime.strptime(time1, "%Y-%m-%d %H:%M")
        dt2 = datetime.strptime(time2, "%Y-%m-%d %H:%M")
        if dt1 <= dt2:
            return True
        else:
            return False

    def confirm_sn_is_selected(self, ele_sn):
        now_time = time.time()
        while True:
            if ele_sn.get_attribute("class") == "selected":
                break
            else:
                ele_sn.click()
            if time.time() > self.return_end_time(now_time):
                assert False, "@@@无法选中device sn, 请检查！！！"
            time.sleep(1)








