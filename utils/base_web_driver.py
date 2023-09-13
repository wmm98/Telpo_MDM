import utils as pack


class BaseWebDriver:
    def __init__(self):
        pass

    def open_web_site(self, url):
        try:
            global driver

            chrome_options = pack.Options()
            chrome_options.add_argument("--allow-insecure-localhost")  # 允许访问不安全的本地主机（可选）
            chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
            driver = pack.webdriver.Chrome(options=chrome_options)

            # driver = webdriver.Chrome()
            driver.implicitly_wait(5)
            driver.maximize_window()
            # url = 'http://test.telpoai.com/login'
            url = url
            # 窗口最大化
            driver.get(url)
            now_time = pack.time.time()
            while True:
                if driver.execute_script('return document.readyState;') == 'complete':
                    break
                if pack.time.time() > now_time + 60:
                    driver.refresh()
                    break
                pack.time.sleep(1)
        except pack.WebDriverException:
            raise Exception("@@@@谷歌驱动异常或者电脑没连接网络！！！！")

    def get_web_driver(self):
        return driver

    def test_network_connection(self):
        url = 'https://www.baidu.com'
        response = pack.requests.get(url)
        if response.status_code != 200:
            return False
        else:
            return True


if __name__ == '__main__':
    case = BaseWebDriver()
    case.open_web_site("")
    case.get_web_driver()
