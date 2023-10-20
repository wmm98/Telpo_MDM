from utils.base_web_driver import BaseWebDriver
from Common import Log
from Page.Devices_Page import DevicesPage
from Page.Catch_Log_Page import CatchLogPage
from Page.Android_Aimdm_Page import AndroidAimdmPage
import time

log = Log.MyLog()


class Optimize_Case:

    def __init__(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = DevicesPage(self.driver, 40)
        self.cat_log_page = CatchLogPage(self.driver, 40)

    def check_single_device(self, sn):
        try:
            self.page.go_to_new_address("devices")
            self.page.search_device_by_sn(sn)
            devices_list = self.page.get_dev_info_list()
            if len(devices_list) == 0:
                e = "@@@@还没有添加该设备 %s， 请检查！！！" % sn
                log.error(e)
                assert False, e
            if "Off" in devices_list[0]["Status"]:
                self.page.refresh_page()
                if "Off" in self.page.get_dev_info_list()[0]:
                    err = "@@@@%s: 设备不在线， 请检查！！！" % sn
                    log.error(err)
                    assert False, err
            return devices_list
        except Exception as e:
            print(e)
            self.page.search_device_by_sn(sn)
            devices_list = self.page.get_dev_info_list()
            if len(devices_list) == 0:
                e = "@@@@还没有添加该设备 %s， 请检查！！！" % sn
                log.error(e)
                assert False, e
            if "Off" in devices_list[0]["Status"]:
                err = "@@@@%s: 设备不在线， 请检查！！！" % sn
                log.error(err)
                assert False, err
            return devices_list

    def get_single_device_list(self, sn):
        try:
            self.page.search_device_by_sn(sn)
            devices_list = self.page.get_dev_info_list()
            return devices_list
        except Exception as e:
            print(e)
            self.page.search_device_by_sn(sn)
            devices_list = self.page.get_dev_info_list()
            return devices_list

    def catch_logs(self, sn, duration, time_out=600):
        self.page.go_to_new_address("devices")
        self.check_single_device(sn)
        send_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        self.page.click_dropdown_btn()
        self.page.time_sleep(2)
        # check the logs list before catch log
        self.page.catch_all_log(duration)
        # select log_type
        self.page.go_to_new_address("catchlog/task")
        # check catch log info
        now_time = self.page.get_current_time()
        while True:
            if len(self.cat_log_page.get_latest_catch_log_list(send_time, sn)) == 1:
                break
            else:
                self.page.refresh_page()
            # wait 20 min
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                assert False, "@@@@超过 60s 还没有相应的catch log！！！"
            self.page.time_sleep(2)

        success_flag = self.page.remove_space(self.page.upper_transfer("Success"))
        report_flag = self.page.remove_space(self.page.upper_transfer("Reporting"))
        fail_flag = self.page.remove_space_and_upper("Failed")
        now_time = self.page.get_current_time()
        while True:
            if len(self.cat_log_page.get_latest_catch_log_list(send_time, sn)) != 0:
                action = self.page.remove_space_and_upper(self.cat_log_page.get_latest_catch_log_list(send_time, sn)[0]["Action"])
                if report_flag in action or success_flag in action:
                    break
                elif fail_flag in action:
                    assert False, "@@@@日志文件上传失败！！！"
                else:
                    self.page.refresh_page()
                # wait 20 min
            if self.page.get_current_time() > self.page.return_end_time(now_time, time_out):
                assert False, "@@@@超过 %ss 还没有采集完 %s分钟的log！！！" % (time_out, duration)
            self.page.time_sleep(3)

        now_time = self.page.get_current_time()
        while True:
            if len(self.cat_log_page.get_latest_catch_log_list(send_time, sn)) != 0:
                action = self.page.remove_space_and_upper(
                    self.cat_log_page.get_latest_catch_log_list(send_time, sn)[0]["Action"])
                print(action)
                if success_flag in action:
                    break
                elif fail_flag in action:
                    assert False, "@@@@日志文件上传失败！！！"
                else:
                    self.page.refresh_page()
            # wait 20 min
            if self.page.get_current_time() > self.page.return_end_time(now_time, time_out):
                assert False, "@@@@超过 %s 还没有上传完 %s分钟的log！！！" % (time_out, duration)
            self.page.time_sleep(3)

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
