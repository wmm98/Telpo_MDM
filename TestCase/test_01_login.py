import TestCase
import allure
import pytest

log = TestCase.MyLog()


class TestLogin:

    def setup_class(self):
        self.driver = TestCase.test_driver
        self.mdm_page = TestCase.MDMPage(self.driver, 40)
        self.wait_times = 10

    def teardown_class(self):
        pass

    @allure.feature('MDM_test02_login')
    @allure.title("login is ok")  # 设置case的名字
    @pytest.mark.dependency(name="test_login_ok", scope='package')
    def test_login_ok(self):
        username = "mdm_automation"
        password = "123456"

        login_ok_title = "Telpo MDM"
        login_ok_url = "http://test.telpoai.com/device/map"
        try:
            self.mdm_page.input_user_name(username)
            self.mdm_page.input_pwd_value(password)
            self.mdm_page.choose_agree_btn()
            self.mdm_page.click_login_btn()
            assert self.mdm_page.web_driver_wait_until(TestCase.EC.url_to_be(login_ok_url))
            assert self.mdm_page.web_driver_wait_until(TestCase.EC.title_is(login_ok_title))
        except AssertionError:
            e = "@@@登录失败， 请检查！！！"
            log.error(e)
            assert False, e
        except Exception:
            e = "@@@用例失败， 请检查！！！"
            log.error(e)
            assert False, e

        # 捕捉弹框提示内容,成功时候可以定位到，失败的时候定位不到, 留在后面解决
        # loc = (By.CLASS_NAME, "toast-message")
        # WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(loc))
        # msg = self.driver.find_element(*loc)
        # print(msg.text)


if __name__ == '__main__':
    case = TestLogin()
    case.test_login_ok()
