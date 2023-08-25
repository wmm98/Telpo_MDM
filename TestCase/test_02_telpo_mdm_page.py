import allure
from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Telpo_MDM_Page import TelpoMDMPage

log = Log.MyLog()


class TestTelpoMDM:

    def setup_class(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = TelpoMDMPage(self.driver, 40)
        self.wait_times = 10

    def teardown_class(self):
        pass

    @allure.feature('MDM_test01 -- not run right now')
    @allure.title("Telpo_MDM main Page")  # 设置case的名字
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.dependency(name="test_TelpoMdM_Page", scope='package')
    def test_Telpo_page(self):
        exp_main_title = "Devices Map"
        try:
            # 验证当前页面
            log.info("当前页面标题为 %s" % self.driver.title)
            act_main_title = self.page.get_loc_main_title()
            assert exp_main_title in act_main_title
            log.info("当前默认的副标题为：%s" % act_main_title)
        except Exception as e:
            log.error(str(e))
            assert False





