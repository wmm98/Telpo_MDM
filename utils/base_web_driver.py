from selenium import webdriver


class BaseWebDriver:
    def __init__(self):
        pass

    def open_web_site(self):
        global driver
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        driver.maximize_window()
        url = 'https://mdm.telpoai.com/login'
        # 窗口最大化
        driver.get(url)

    def get_web_driver(self):
        return driver


if __name__ == '__main__':
    case = BaseWebDriver()
    case.open_web_site()
    case.get_web_driver()
