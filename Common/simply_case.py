from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Devices_Page import DevicesPage

log = Log.MyLog()


class Optimize_Case:
    def __init__(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = DevicesPage(self.driver, 40)

    def check_single_device(self, sn):
        self.page.search_device_by_sn(sn)
        devices_list = self.page.get_dev_info_list()
        if len(devices_list) == 0:
            e = "@@@@还没有添加该设备 %s， 请检查！！！" % sn
            log.error(e)
            assert False, e
        if devices_list[0]["Status"] == "Off":
            err = "@@@@%s: 设备不在线， 请检查！！！" % sn
            log.error(err)
            assert False, err

    def get_single_device_list(self, sn):
        self.page.search_device_by_sn(sn)
        devices_list = self.page.get_dev_info_list()
        return devices_list

    def check_alert_text(self, exp_text):
        try:
            print("预期结果：", exp_text)
            text = self.page.get_alert_text()
            print("实际结果：", text)
            if exp_text in text:
                log.info("信息发送失败成功， 请检查设备信息")
                return True
            else:
                return False
        except Exception:
            return False

