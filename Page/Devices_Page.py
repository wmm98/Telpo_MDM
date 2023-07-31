from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DevicesPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)

    loc_category_btn = (By.XPATH, "/html/body/div[1]/div[1]/section/div/div[1]/div[11]/div[1]/a[1]")
    loc_input_cate_box = (By.XPATH, "//*[@id=\"category_name\"]")
    loc_save_btn_cate = (By.XPATH, "//*[@id=\"modal-add-category\"]/div/div/div[3]/button[2]")

    loc_mode_btn = (By.XPATH, "/html/body/div[1]/div[1]/section/div/div[1]/div[11]/div[1]/a[2]")
    loc_input_mode_box = (By.XPATH, "//*[@id=\"model_name\"]")
    loc_save_btn_mode = (By.XPATH, "//*[@id=\"modal-add-model\"]/div/div/div[3]/button[2]")

    def click_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))
        self.click(self.loc_category_btn)

    def add_category(self, cate_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_cate_box))
        self.input_text(self.loc_input_cate_box, cate_name)
        self.click(self.loc_save_btn_cate)

    def click_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))
        self.click(self.loc_mode_btn)

    def add_model(self, model_name):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_mode_box))
        self.input_text(self.loc_input_mode_box, model_name)
        self.click(self.loc_save_btn_mode)














































