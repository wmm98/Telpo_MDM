from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DevicesPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    loc_category_btn = (By.XPATH, "/html/body/div[1]/div[1]/section/div/div[1]/div[11]/div[1]/a[1]")
    loc_input_cate_box = (By.XPATH, "//*[@id=\"category_name\"]")
    loc_save_btn_cate = (By.XPATH, "//*[@id=\"modal-add-category\"]/div/div/div[3]/button[2]")
    loc_close_btn_cate = (By.XPATH, "//*[@id=\"modal-add-category\"]/div/div/div[3]/button[1]")

    loc_mode_btn = (By.XPATH, "/html/body/div[1]/div[1]/section/div/div[1]/div[11]/div[1]/a[2]")
    loc_input_mode_box = (By.XPATH, "//*[@id=\"model_name\"]")
    loc_save_btn_mode = (By.XPATH, "//*[@id=\"modal-add-model\"]/div/div/div[3]/button[2]")
    loc_close_btn_mode = (By.XPATH, "//*[@id=\"modal-add-model\"]/div/div/div[3]/button[1]")

    # 重复提示框
    loc_name_already_existed = (By.XPATH, "//*[@id=\"swal2-title\"]")

    # Model盒子
    loc_models_box = (By.XPATH, "/html/body/div[1]/div[1]/section/div/div[1]/div[11]/div[1]/div[8]")
    loc_model_list = (By.TAG_NAME, "a")

    def get_models_list(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_models_box))
        eles = self.get_elements_in_range(self.loc_models_box, self.loc_model_list)
        models_list = [ele.text for ele in eles]
        return models_list

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

    def get_name_existed_text(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_name_already_existed))
        return ele.text

