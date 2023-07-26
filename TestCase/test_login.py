import time

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


class TestLogin:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        url = 'https://mdm.telpoai.com/login'
        # 窗口最大化
        self.driver.get(url)

    def test_login_ok(self):
        username = "ceshibu"
        password = "123456"

        loc_pwd = (By.ID, "password")
        loc_user = (By.ID, "username")
        # 用户名
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc_user))
        self.driver.find_element(*loc_user).clear()
        self.driver.find_element(*loc_user).send_keys(username)
        time.sleep(3)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc_pwd))
        self.driver.find_element(*loc_pwd).clear()
        self.driver.find_element(*loc_pwd).send_keys(password)
        time.sleep(3)

        loc_agree = (By.XPATH, "//*[@id=\"agreeTerms\"]")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc_agree)).send_keys(Keys.SPACE)
        print(self.driver.find_element(*loc_agree).is_selected())
        time.sleep(2)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc_agree)).send_keys(Keys.SPACE)

        # res = self.driver.find_elements(By.CSS_SELECTOR, "#agreeTerms")
        # print(res)
        # res[0].send_keys(Keys.SPACE)
        time.sleep(5)

        loc_login = (By.XPATH, "//*[@id=\"loginform\"]/div[3]/a")
        # self.driver.find_element().click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc_login)).click()
        # print(res)
        time.sleep(10)

        self.driver.quit()


if __name__ == '__main__':
    case = TestLogin()
    case.test_login_ok()
