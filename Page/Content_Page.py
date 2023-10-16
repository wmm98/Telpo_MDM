import Page as public_pack
from Page.Telpo_MDM_Page import TelpoMDMPage

By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time
log = public_pack.MyLog()
conf = public_pack.Config()


class ContentPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_content_list = (By.ID, "fgdata")

    # search related
    loc_search_box_show = (By.CSS_SELECTOR, "[class = 'fd-panel-search']")  # open status  display: inline-block;  default status: display: none;
    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_files_type = (By.CSS_SELECTOR, "[class = 'form-control form-control-sm file-search-usefor']")
    loc_input_name_box = (By.CSS_SELECTOR, "[class = 'form-control file-search-name']")

    def search_content(self, file_type, file_name):
        try:
            search_ele = self.get_element(self.loc_search_box_show).find_element(self.loc_search_btn)
            search_ele.click()
            self.confirm_search_box_show()
            self.select_file_type(file_type)
            self.input_text(self.confirm_search_box_show(), file_name)
            self.time_sleep(1)
            ensure_ele = self.get_element(self.loc_search_box_show).find_element(self.loc_search_btn)
            ensure_ele.click()
            self.confirm_search_box_fade()
        except Exception as e:
            print(e)
        # except public_pack.ElementNotInteractableException:
        #     search_ele = self.get_element(self.loc_search_box_show).find_element(self.loc_search_btn)
        #     search_ele.click()
        #     self.confirm_search_box_show()
        #     self.select_file_type(file_type)
        #     self.input_text(self.confirm_search_box_show(), file_name)
        #     self.time_sleep(1)
        #     ensure_ele = self.get_element(self.loc_search_box_show).find_element(self.loc_search_btn)
        #     ensure_ele.click()
        #     self.confirm_search_box_fade()

    def select_file_type(self, file_type):
        self.select_by_text(self.loc_files_type, file_type)

    def get_ota_package_list(self):
        if "NO Data" in self.get_element(self.loc_content_list).text:
            return []
        else:
            boxes = self.get_elements(self.loc_content_list)
            return boxes

    def confirm_search_box_show(self):
        now_time = self.get_current_time()
        while True:
            if "inline-block" in self.get_element(self.loc_search_box_show).get_attribute("style"):
                break
            else:
                self.ele_is_existed_in_range(self.loc_search_box_show, self.loc_search_btn)
                ele = self.get_element(self.loc_search_box_show).find_element(self.loc_search_btn)
                ele.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法打开搜索框， 请检查！！！！"
            self.time_sleep(1)

    def confirm_search_box_fade(self):
        now_time = self.get_current_time()
        while True:
            if "none" in self.get_element(self.loc_search_box_show).get_attribute("style"):
                break
            else:
                self.ele_is_existed_in_range(self.loc_search_box_show, self.loc_search_btn)
                ele = self.get_element(self.loc_search_box_show).find_element(self.loc_search_btn)
                ele.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@无法进行搜索， 请检查！！！！"
            self.time_sleep(1)
