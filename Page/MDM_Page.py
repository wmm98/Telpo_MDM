import Page
By = Page.By
EC = Page.EC
t_time = Page.time
keys = Page.Keys


class MDMPage(Page.BasePage):

    def __init__(self, driver, times):
        Page.BasePage.__init__(self, driver, times)

    agree_key = keys.SPACE
    loc_pwd_btn = (By.ID, "password")
    loc_user_btn = (By.ID, "username")
    loc_agree_btn = (By.XPATH, "//*[@id=\"agreeTerms\"]")  # //*[@id="agreeTerms"]
    loc_login_btn = (By.XPATH, "//*[@id=\"loginform\"]/div[3]/a")

    loc_success_tips = (By.ID, "swal2-title")

    def input_user_name(self, username):
        self.input_text(self.loc_user_btn, username)

    def input_pwd_value(self, password):
        self.input_text(self.loc_pwd_btn, password)

    def choose_agree_btn(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_agree_btn))
        self.input_keyboard(self.loc_agree_btn, self.agree_key)
        now_time = t_time.time()
        while True:
            if self.ele_is_selected(ele):
                break
            else:
                self.input_keyboard(self.loc_agree_btn, self.agree_key)
            t_time.sleep(1)
            if t_time.time() > self.return_end_time(now_time):
                assert False, "@@@无法选中check box, 请检查！！！"

    def click_login_btn(self):
        self.click(self.loc_login_btn)
        self.confirm_tips_alert_show(self.loc_login_btn)
        # self.

    def confirm_tips_alert_show(self, loc):
        now_time = t_time.time()
        while True:
            if self.get_tips_alert():
                break
            else:
                self.click(loc)
            if t_time.time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭，请检查！！！"

    def get_tips_alert(self):
        try:
            ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_success_tips), 5)
            print(ele.text)
            return True
        except Page.TimeoutException:
            return False


# if __name__ == '__main__':
#     from selenium import webdriver
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(30)
#     driver.maximize_window()
#     url = 'https://mdm.telpoai.com/login'
#     # 窗口最大化
#     MDMPage(driver)
#     driver.get(url)








