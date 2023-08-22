from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseWebDriver:
    def __init__(self):
        pass

    def open_web_site(self, url):
        global driver

        chrome_options = Options()
        chrome_options.add_argument("--allow-insecure-localhost")  # 允许访问不安全的本地主机（可选）
        chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        driver.maximize_window()
        # url = 'http://test.telpoai.com/login'
        url = url
        # 窗口最大化
        driver.get(url)

    def get_web_driver(self):
        return driver


if __name__ == '__main__':
    case = BaseWebDriver()
    case.open_web_site("")
    case.get_web_driver()
