from Page.Base_Page import BasePage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MDMPage(BasePage):

    def __init__(self, driver, times):
        BasePage.__init__(self, driver, times)

    agree_key = Keys.SPACE
    loc_pwd_btn = (By.ID, "password")
    loc_user_btn = (By.ID, "username")
    loc_agree_btn = (By.XPATH, "//*[@id=\"agreeTerms\"]")  # //*[@id="agreeTerms"]
    loc_login_btn = (By.XPATH, "//*[@id=\"loginform\"]/div[3]/a")

    def input_user_name(self, username):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_user_btn))
        self.input_text(self.loc_user_btn, username)

    def input_pwd_value(self, password):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_pwd_btn))
        self.input_text(self.loc_pwd_btn, password)

    def choose_agree_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_agree_btn))
        self.input_keyboard(self.loc_agree_btn, self.agree_key)

    def click_login_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_login_btn))
        self.click(self.loc_login_btn)


# if __name__ == '__main__':
#     from selenium import webdriver
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(30)
#     driver.maximize_window()
#     url = 'https://mdm.telpoai.com/login'
#     # 窗口最大化
#     MDMPage(driver)
#     driver.get(url)








