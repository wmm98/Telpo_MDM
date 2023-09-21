import Page as public_pack
from Page.Telpo_MDM_Page import TelpoMDMPage

By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time
log = public_pack.MyLog()
conf = public_pack.Config()


class CatchLogPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_data_body = (By.ID, "catchlog-list")
    loc_single_log = (By.TAG_NAME, "tr")
    loc_single_release_col = (By.TAG_NAME, "td")
    loc_small_col = (By.TAG_NAME, "small")

    # def finish_catch_log(self, log_info):
    #     self.

    def get_latest_catch_log_list(self, send_time, serial, log_type="all"):
        self.page_load_complete()
        get_type = self.get_log_type(log_type)
        release_list = self.get_element(self.loc_data_body)
        logs_list = []
        existed = self.ele_is_existed_in_range(self.loc_data_body, self.loc_single_log)
        if not existed:
            self.time_sleep(2)
            existed = self.ele_is_existed_in_range(self.loc_data_body, self.loc_single_log)
        if self.remove_space("No Dat") in self.remove_space(release_list.text):
            return []
        if existed:
            logs = release_list.find_elements(*self.loc_single_log)
            for single_log in logs:
                cols = single_log.find_elements(*self.loc_single_release_col)
                receive_time_text = cols[4].find_elements(*self.loc_small_col)[1].text
                # duration = cols[4].find_elements(*self.loc_small_col)[3].get_attribute("data-time")
                sn = cols[2].text
                log_type = self.remove_space(self.upper_transfer(cols[3].text))   # cols[3].text
                time_line = self.extract_integers(receive_time_text)
                receive_time = self.format_string_time(time_line)
                action = self.remove_space(self.upper_transfer(cols[6].text))
                if self.compare_time(send_time, receive_time):
                    # check if log type is right
                    for t in list(get_type.values()):
                        t = self.upper_transfer(t)
                        if t not in log_type:
                            return []
                    if serial in sn:
                        # logs_list.append(single_log)
                        logs_list.append({"SN": sn, "Catch_Time": receive_time, "Action": action})
            return logs_list
        else:
            return []

    def get_log_type(self, log_type):
        if log_type == "all":
            return {"app": "app", "system": "system"}
        elif log_type == "app":
            return {"app": "app"}
        elif log_type == "system":
            return {"system": "system"}
        else:
            return {"app": "app", "system": "system"}