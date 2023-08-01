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

data_list = [{"cate": "手持终端", "model": "TPS900P"},
             {"cate": "壁挂式", "model": "TPS980P"}]


class TestDevicesPage:
    def setup_class(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = DevicesPage(self.driver, 40)

    def teardown_class(self):
        pass

    @allure.feature('MDM_test01')
    @allure.title("Devices main page")  # 设置case的名字
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

    @allure.feature('MDM_test01--no test now ')
    @allure.title("Devices-add category and  model")  # 设置case的名字
    @pytest.mark.parametrize('cate_model', data_list)
    def test_add_category_model(self, cate_model):
        exp_existed_name = "name already existed"

        self.page.click_category()
        self.page.add_category(cate_model["cate"])
        name = self.page.get_name_existed_text()
        print(name)
        if name == exp_existed_name:
            self.page.close_btn_cate()

        # self.page.click_model()
        # self.page.add_model(cate_model["model"])

        time.sleep(2)
        self.page.get_loc_main_title()
        self.page.find_category()
        self.page.find_model()

    @allure.feature('MDM_test01')
    @allure.title("Devices-debug")  # 设置case的名字
    def test_devices_test(self):
        print(self.page.get_models_list())





