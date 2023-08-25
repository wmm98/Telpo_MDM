import Page

By = Page.By
EC = Page.EC
t_time = Page.time

log = Page.MyLog()


class ReleaseDevicePage(Page.DevicesPage, Page.MDMPage):

    def __init__(self, driver, times):
        Page.DevicesPage.__init__(self, driver, times)
        self.driver = driver

    def login_release_version(self, user_info, login_ok_title):
        # username = "ceshibu03"
        # password = "123456"

        # login_ok_title = "Telpo MDM"
        # login_ok_url = "http://test.telpoai.com/device/map"
        now_time = t_time.time()
        while True:
            self.input_user_name(user_info["username"])
            self.input_pwd_value(user_info["password"])
            self.choose_agree_btn()
            self.click_login_btn()
            text = self.get_alert_text()
            if "success" in text:
                break
            else:
                self.refresh_page()
            if t_time.time() > self.return_end_time(now_time):
                e = "@@@@ 3分钟内多次登录， 登录失败， 请检查！！！"
                log.error(e)
                assert False, e
            t_time.sleep(1)
            self.refresh_page()
            # if login_ok_title in self.get_title():
            #     break
            # else:
            #     self.refresh_page()
            # if time.time() > self.return_end_time():
            #     e = "@@@@ 3分钟内多次加载页面， 加载失败， 请检查！！！"
            #     log.error(e)
            #     assert False, e
            # time.sleep(1)

    def go_to_device_page(self, top_title):
        self.click_devices_btn()
        now_time = t_time.time()
        while True:
            if top_title in self.get_loc_main_title():
                break
            else:
                self.click_devices_btn()
            if t_time.time() > self.return_end_time(now_time):
                e = "@@@@ 3分钟内多次加载页面， 加载失败， 请检查！！！"
                log.error(e)
                assert False, e
            t_time.sleep(1)

    def get_single_device_list_release(self, sn):
        self.search_device_by_sn(sn)
        devices_list = self.get_dev_info_list()
        return devices_list
