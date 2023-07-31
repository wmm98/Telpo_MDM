from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DevicesPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)

    category_cls_name = "btn btn-primary btn-block mb-3 add_new_category"
    loc_category_btn = (By.CLASS_NAME, category_cls_name)
    loc_input_cate_box = (By.CLASS_NAME, "category_name")
    loc_save_btn = (By.CLASS_NAME, "btn btn-primary create_category_button")

    def click_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))
        self.click(self.loc_category_btn)

    def input_category_name(self, cate_name):
        self.input_text(self.loc_input_cate_box, cate_name)

    def click_save(self):
        self.click(self.loc_save_btn)






































