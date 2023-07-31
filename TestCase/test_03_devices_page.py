import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Devices_Page import DevicesPage
import time
from selenium.webdriver.support import expected_conditions as EC

log = Log.MyLog()


class TestDevicesPage:

    def setup_class(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = DevicesPage(self.driver, 40)

    def teardown_class(self):
        pass

    @allure.feature('MDM_test01')
    @allure.title("Devices页面")  # 设置case的名字
    @pytest.mark.dependency(depends=["test_TelpoMdM_Page"], scope='package')
    def test_go_to_devices_page(self):
        exp_main_title = "Total Devices"
        try:
            self.page.click_devices_btn()
            # 验证当前页面
            act_main_title = self.page.get_loc_main_title()
            assert exp_main_title in act_main_title
            log.info("当前默认的副标题为：%s" % act_main_title)
        except Exception as e:
            log.error(str(e))
            assert False

    @allure.feature('MDM_test01')
    @allure.title("Devices-添加种类")  # 设置case的名字
    @pytest.mark.parametrize('cate_text, model_text', [["手持终端", "TPS900"], ["壁挂式", "TPS980P"]])
    def test_add_category(self, cate_text, model_text):
        # cate_text = "手持终端"
        # model_text = "TPS900"

        self.page.click_category()
        self.page.add_category(cate_text)

        self.page.click_model()
        self.page.add_model(model_text)








