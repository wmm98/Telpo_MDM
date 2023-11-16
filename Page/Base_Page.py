import Page as public_pack
from Page.Interface_Page import interface

test_yml = public_pack.yaml_data


class BasePage(interface):

    def __init__(self, driver, times):
        self.driver = driver
        self.times = times

    loc_tips = (public_pack.By.ID, "swal2-title")

    def get_html_text(self):
        # 获取页面的 HTML 代码
        html = self.driver.page_source

        # 使用 BeautifulSoup 解析 HTML 代码
        soup = public_pack.BeautifulSoup(html, 'html.parser')

        # 查找页面中的文本
        text = soup.get_text()
        return text

    def go_to_new_address(self, url):
        address = "%s/%s" % (test_yml["website_info"]["test_base_url"], url)
        self.driver.get(address)
        now_time = self.get_current_time()
        if self.driver.current_url != address:
            while True:
                if self.driver.current_url == address:
                    break
                else:
                    self.driver.get(address)
                if self.get_current_time() > self.return_end_time(now_time):
                    assert False, "@@@打开 %s 失败， 请检查！！！" % address
                self.time_sleep(1)
        self.page_load_complete()

    def get_current_window_url(self):
        return self.driver.current_url

    def quit_browser(self):
        self.driver.quit()

    def comm_alert_fade(self, loc):
        try:
            self.web_driver_wait_until_not(public_pack.EC.presence_of_element_located(loc), 5)
            return True
        except public_pack.TimeoutException:
            return False

    def comm_alert_show(self, loc):
        try:
            self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc), 5)
            return True
        except public_pack.TimeoutException:
            return False

    def comm_confirm_alert_not_existed(self, alert_loc, ele_loc, ex_js=0):
        now_time = self.get_current_time()
        while True:
            if self.comm_alert_fade(alert_loc):
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(ele_loc)
                else:
                    self.click(ele_loc)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭 出错， 请检查！！！"
            self.time_sleep(1)

    def confirm_alert_not_existed(self, loc, ex_js=0):
        now_time = self.get_current_time()
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
                if self.get_current_time() > self.return_end_time(now_time):
                    assert False, "@@@@弹窗无法关闭 出错， 请检查！！！"
            self.time_sleep(1)

    def confirm_alert_existed(self, loc, ex_js=0):
        now_time = self.get_current_time()
        while True:
            if self.alert_is_existed():
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法打开 出错， 请检查！！！"
            self.time_sleep(1)

    def alert_is_existed(self):
        if public_pack.EC.alert_is_present():
            return True
        else:
            return False

    def alert_is_not_existed(self):
        if public_pack.EC.alert_is_present():
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
        except public_pack.TimeoutException:
            return False

    def page_is_loaded(self):
        if self.driver.execute_script('return document.readyState;') == 'complete':
            return True
        else:
            return False

    def page_load_complete(self):
        now_time = self.get_current_time()
        while True:
            if self.page_is_loaded():
                break
            print("网页还没有加载完成")
            if self.get_current_time() > self.return_end_time(now_time, 60):
                self.refresh_page()
                break
            self.refresh_page()
            self.time_sleep(2)

    def move_and_click(self, ele):
        public_pack.ActionChains(self.driver).move_to_element(ele).click().perform()

    def move_to_element(self, ele):
        public_pack.ActionChains(self.driver).move_to_element(ele).perform()

    def refresh_page(self):
        self.driver.refresh()
        public_pack.t_time.sleep(1)

    def get_selector(self, loc):
        ele = self.get_element(loc)
        select = public_pack.Select(ele)
        return select

    def exc_js_click(self, ele):
        self.driver.execute_script("arguments[0].click();", ele)

    def exc_js_click_loc(self, loc):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc))
        ele = self.get_element(loc)
        self.driver.execute_script("arguments[0].click();", ele)

    def deal_ele_selected(self, ele):
        now_time = self.get_current_time()
        while True:
            if self.ele_is_selected(ele):
                break
            else:
                self.exc_js_click(ele)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法选中check box, 请检查！！！"
            self.time_sleep(1)

    def deal_ele_not_selected(self, ele):
        now_time = self.get_current_time()
        while True:
            if not self.ele_is_selected(ele):
                break
            else:
                self.exc_js_click(ele)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法选中check box, 请检查！！！"
            self.time_sleep(1)

    def ele_is_selected(self, ele):
        return ele.is_selected()

    def select_by_text(self, loc, value):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc))
        select = self.get_selector(loc)
        # select.select_by_value(value)
        select.select_by_visible_text(value)

    def select_by_value(self, loc, value):
        select = self.get_selector(loc)
        select.select_by_value(value)

    def get_element(self, loc):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc))
        ele = self.driver.find_element(*loc)
        # self.driver.execute_script("arguments[0].style.backgroundColor = 'yellow'", ele)
        # self.move_to_element(ele)
        return ele

    def get_elements(self, loc):
        self.web_driver_wait_until(public_pack.EC.presence_of_all_elements_located(loc))
        return self.driver.find_elements(*loc)

    def get_elements_in_range(self, loc_pre, loc_pos):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc_pre))
        return self.driver.find_element(*loc_pre).find_elements(*loc_pos)

    def input_text(self, loc, text, clear=True):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc))
        ele = self.get_element(loc)
        if clear:
            ele.clear()
        ele.send_keys(text)

    def input_keyboard(self, loc, keyboard):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc))
        ele = self.get_element(loc)
        ele.send_keys(keyboard)

    def click(self, loc):
        self.web_driver_wait_until(public_pack.EC.presence_of_element_located(loc))
        ele = self.driver.find_element(*loc)
        # self.driver.execute_script("arguments[0].style.backgroundColor = 'yellow'", ele)
        # self.move_to_element(ele)
        ele.click()

    def get_title(self):
        return self.driver.title

    def service_unavailable_list(self):
        return ["503", "302"]

    def web_driver_wait_until(self, condition, wait_times=0):
        if wait_times == 0:
            return public_pack.WebDriverWait(self.driver, self.times).until(condition)
        else:
            return public_pack.WebDriverWait(self.driver, wait_times).until(condition)

    def web_driver_wait_until_not(self, condition, wait_times=0):
        if wait_times == 0:
            return public_pack.WebDriverWait(self.driver, self.times).until_not(condition)
        else:
            return public_pack.WebDriverWait(self.driver, wait_times).until_not(condition)

    def check_ele_is_selected(self, ele):
        if not self.ele_is_selected(ele):
            self.web_driver_wait_until(public_pack.EC.element_to_be_selected(ele))

    def check_ele_is_not_selected(self, ele):
        if self.ele_is_selected(ele):
            self.web_driver_wait_until_not(public_pack.EC.element_to_be_selected(ele))

    def switch_to_alert(self):
        al = self.driver.switch_to.alert
        return al

    def confirm_sn_is_selected(self, ele_sn):
        now_time = self.get_current_time()
        while True:
            if ele_sn.get_attribute("class") == "selected":
                break
            else:
                ele_sn.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法选中device sn, 请检查！！！"
            self.time_sleep(1)

    def confirm_tips_alert_show(self, loc, timeout=6):
        now_time = self.get_current_time()
        while True:
            if self.get_tips_alert(timeout):
                break
            else:
                self.click(loc)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭，请检查！！！"
            self.time_sleep(1)

    def get_tips_alert(self, timeout=6):
        try:
            ele = self.web_driver_wait_until(public_pack.EC.presence_of_element_located(self.loc_tips), timeout)
            print(ele.text)
            return True
        except public_pack.TimeoutException:
            return False

    def get_action_status(self, action):
        """
                Upgrade action (1: downloading, 2: downloading complete, 3: upgrading,
                 4: upgrading complete, 5: downloading failed, 6: upgrading failed)
                 0: Uninstall completed
        """
        action = self.upper_transfer(self.remove_space(action))
        if self.upper_transfer(self.remove_space("Uninstall completed")) in action:
            return 0
        if self.upper_transfer(self.remove_space("Downloading")) in action:
            return 1
        if self.upper_transfer(self.remove_space("Download Completed")) in action:
            return 2
        if self.upper_transfer(self.remove_space("Upgrading")) in action:
            return 3
        if self.upper_transfer(self.remove_space("Upgrade completed")) in action:
            return 4
        if self.upper_transfer(self.remove_space("Download Fail")) in action:
            return 5
        if self.upper_transfer(self.remove_space("Upgrade Fail")) in action:
            return 6
        if self.upper_transfer(self.remove_space("Process completed")) in action:
            return 7
