import time
import allure
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common.element_operations import ElementsOperations
from utils.base_web_driver import BaseWeb
import pytest


class TestLogin:

    def setup_class(self):
        # self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        # self.driver.maximize_window()
        # url = 'https://mdm.telpoai.com/login'
        # # 窗口最大化
        # self.driver.get(url)

        self.driver = BaseWeb().driver
        self.element_func = ElementsOperations(self.driver)
        self.wait_times = 10

    def teardown_class(self):
        pass

    @allure.feature('MDM_test01')
    @allure.title("登录成功测试")  # 设置case的名字
    @pytest.mark.dependency(name="test_login_ok", scope='package')
    def test_login_ok(self):
        username = "ceshibu"
        password = "123456"
        agree_key = Keys.SPACE

        loc_pwd_btn = (By.ID, "password")
        loc_user_btn = (By.ID, "username")
        loc_agree_btn = (By.XPATH, "//*[@id=\"agreeTerms\"]")  # //*[@id="agreeTerms"]
        loc_login_btn = (By.XPATH, "//*[@id=\"loginform\"]/div[3]/a")
        login_ok_title = "Telpo MDM"
        login_ok_url = "https://mdm.telpoai.com/device/map"

        # 用户名
        self.element_func.web_driver_wait_until(EC.presence_of_element_located(loc_user_btn))
        self.element_func.element_send_keys(loc_user_btn, username)
        # 密码
        self.element_func.web_driver_wait_until(EC.presence_of_element_located(loc_pwd_btn))
        self.element_func.element_send_keys(loc_pwd_btn, password)

        # 同意
        self.element_func.web_driver_wait_until(EC.presence_of_element_located(loc_agree_btn))
        self.element_func.element_send_keys_checkbox(loc_agree_btn, agree_key)
        self.element_func.web_driver_wait_until(EC.element_located_to_be_selected(loc_agree_btn))

        # # 登录
        self.element_func.web_driver_wait_until(EC.presence_of_element_located(loc_login_btn))
        self.element_func.element_click(loc_login_btn)

        assert self.element_func.web_driver_wait_until(EC.url_changes(login_ok_url)), \
            "@@@登录没有跳转成功， 页面加载过慢或者登录失败！！！"

        assert self.element_func.web_driver_wait_until(EC.title_is(login_ok_title)), "@@@页面跳失败!!!"

        # assert False

        # 捕捉弹框提示内容,成功时候可以定位到，失败的时候定位不到, 留在后面解决
        # loc = (By.CLASS_NAME, "toast-message")
        # WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(loc))
        # msg = self.driver.find_element(*loc)
        # print(msg.text)

    # @allure.feature('MDM_test01')
    # @allure.title("调试")
    # @pytest.mark.dependency(depends=["login_ok"])
    # def test_login_test(self):
    #     pass
        # print(self.driver.title)
        # assert False
        # res = self.element_func.wait_title_is("Telpo MDM")
        # print(res)
        # res = WebDriverWait(self.driver, 10).until(EC.title_is("Telpo MDM"))
        # print(res)

        # assert self.element_func.web_driver_wait_until(EC.title_is("Telpo MDM")), "@@@页面跳失败!!!"


if __name__ == '__main__':
    case = TestLogin()
    case.test_login_ok()
