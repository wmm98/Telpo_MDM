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

    # 种类text
    loc_cate_box = (By.CLASS_NAME, "category_list")

    # 创建设备
    loc_new_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square text-black']")
    loc_input_dev_name = (By.ID, "device_name")
    loc_input_dev_SN = (By.ID, "device_sn")
    loc_select_dev_cate = (By.ID, "Category")
    loc_select_dev_mode = (By.ID, "Model")
    loc_save_dev_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_create_device_button']")
    loc_close_dev_btn = (By.XPATH, "//*[@id=\"modal-add-device\"]/div/div/div[3]/button[1]")

    loc_devices_list = (By.ID, "device_list")
    loc_tr = (By.TAG_NAME, "tr")
    loc_td = (By.CLASS_NAME, "text-center")

    def click_new_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_new_btn))
        self.click(self.loc_new_btn)
        self.alert_show()

    def add_devices_info(self, dev_info):
        # name
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_input_dev_name))
        self.input_text(self.loc_input_dev_name, dev_info['name'])
        # SN
        self.input_text(self.loc_input_dev_SN, dev_info['SN'])
        # cate
        self.select_by_text(self.loc_select_dev_cate, dev_info['cate'])
        # model
        self.select_by_text(self.loc_select_dev_mode, dev_info['model'])
        # 保存
        self.click(self.loc_save_dev_btn)
        self.alert_fade()

    # 只在一开始的时候运行
    def get_dev_info_list(self):
        try:
            devices_list = []
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_devices_list))
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            for tr_ele in tr_eles:
                td_eles = tr_ele.find_elements(*self.loc_td)[1:8]
                devices_list.append({"Name": td_eles[0].text, "SN": td_eles[4].text, "Status": td_eles[5].text, "Lock Status": td_eles[6].text})
            return devices_list
        except TimeoutException:
            return []

    # 返回devics_list长度
    def get_dev_info_length(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_devices_list))
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            return len(tr_eles)
        except TimeoutException:
            return 0

    def search_device_serial(self, serial):
        pass

    # 判断alert消失
    def alert_fade(self):
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show))

    # 判断alert出现
    def alert_show(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show))

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

    # 获取所有的cate
    def get_categories_list(self):
        try:
            self.web_driver_wait_until(EC.presence_of_all_elements_located(self.loc_cate_box))
            eles = self.get_elements(self.loc_cate_box)
            cates_list = [ele.text for ele in eles]
            print(cates_list)
            return cates_list
        except TimeoutException:
            return []

    # 查找cate, 此处用来作判断
    def find_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))

    # 查找model, 此处用来作判断
    def find_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))

    # 点击cate
    def click_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))
        self.click(self.loc_category_btn)

    # 添加cate
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

    # 获取弹窗文本
    def get_alert_text(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed))
        return ele.text
