from selenium.common import TimeoutException

from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DevicesPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_category_btn = (By.LINK_TEXT, "Create New Category")
    loc_input_cate_box = (By.ID, "category_name")
    loc_save_btn_cate = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_category_button']")
    loc_close_btn_cate = (By.XPATH, "//*[@id=\"modal-add-category\"]/div/div/div[3]/button[1]")

    loc_mode_btn = (By.LINK_TEXT, "Create New Model")
    loc_input_mode_box = (By.ID, "model_name")
    loc_save_btn_mode = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_model_button']")
    loc_close_btn_mode = (By.XPATH, "//*[@id=\"modal-add-model\"]/div/div/div[3]/button[1]")
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")
    loc_mode_name_success = (By.ID, "swal2-title")

    # Model盒子,model list
    loc_models_box = (By.CSS_SELECTOR, "[class = 'modelSelectd model_list']")

    # 创建设备
    loc_new_btn = (By.LINK_TEXT, "New")
    loc_input_dev_name = (By.ID, "device_name")
    loc_input_SN = (By.ID, "device_sn")
    loc_select_cate = (By.ID, "Category")
    loc_select_mode = (By.ID, "Model")



    def alert_fade(self):
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show))

    # 添加设备
    def get_models_list(self):
        try:
            self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_models_box))
            eles = self.get_elements(self.loc_models_box)
            models_list = [ele.text for ele in eles]
            print(models_list)
            return models_list
        except TimeoutException:
            return []

    def find_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))

    def find_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))

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

    def close_btn_mode(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_close_btn_mode))
        self.click(self.loc_close_btn_mode)

    def close_btn_cate(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_close_btn_cate))
        self.click(self.loc_close_btn_cate)

    def get_alert_text(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed))
        return ele.text
