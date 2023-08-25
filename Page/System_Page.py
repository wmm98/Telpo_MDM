import Page

conf = Page.Config()
By = Page.By
EC = Page.EC
t_time = Page.time


class SystemPage(Page.TelpoMDMPage):
    def __init__(self, driver, times):
        Page.TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    # private app related
    loc_system_logs_btn = (By.LINK_TEXT, "System Logs")
    system_log_main_title = "System Log"
    loc_data_body = (By.ID, "databody")
    loc_single_log = (By.TAG_NAME, "tr")
    loc_single_action = (By.TAG_NAME, "td")

    def click_system_log_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_system_logs_btn))
        self.click(self.loc_system_logs_btn)
        self.deal_main_title(self.loc_system_logs_btn, self.system_log_main_title)

    def check_latest_action(self):
        body = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_data_body))
        if "NO Data" in body.text:
            assert False, "@@@@没有任何log, 请检查！！！"

        action = body.find_element(*self.loc_single_log).find_elements(*self.loc_single_action)[2].text
        return action

    def get_latest_action(self):
        self.click_system_btn()
        self.click_system_log_btn()
        action = self.check_latest_action()
        return action
