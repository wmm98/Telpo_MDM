import time

import requests


class RequestMethodCarryFormData:
    """
    定义请求类型
    以表单方式form-data传递参数
    """

    def __init__(self):

        """初始化参数"""
        # self.data = {}
        # self.files = {}
        self.header = {}
        self.address = "http://test.telpopaas.com/"

    def get(self, url, data):
        """
        定义get方法请求
        :return:
        """
        try:
            res = requests.get(url=url, params=data, headers=self.header, timeout=60)
            return res
        except TimeoutError:
            return print('%s get request timeout!' % url)

    def getCarryToken(self, url, data):
        """
        定义get方法请求，额外添加token
        :return:
        """
        try:
            # print(self.header)
            res = requests.get(url=url, params=data, headers=self.header, timeout=60)
            return res.json()
        except Exception:
            return False

    def postCarryToken(self, url, data):
        """
        定义post方法请求
        这个携带json应该不需要额外改
        :return:
        """
        try:
            res = requests.post(url=url, data=data, headers=self.header, timeout=60)
            return res.json()
        except Exception:
            return False

    # just for login
    def post(self, url, data):
        try:
            response = requests.post(url=url, data=data, timeout=60)
            self.header["token"] = response.json()["token"]
            print(":,", self.header)
            return response.json()
        except Exception:
            print("这里出错了")


if __name__ == '__main__':
    url = "http://test.telpopaas.com/login"
    data = {
        "account": "ceshibu",
        "password": "123456",
        "platform": "mdm"
    }
    req = RequestMethodCarryFormData()
    req.post(url, data)
    # time.sleep(5)
    log_url = "http://test.telpopaas.com/appLogs"
    data1 = {"Page": 1, "offset": 30}
    # data1 = {"Page": 1,
    #          "offset": 5,
    #          "share": 0,
    #          "verifyed": 0,
    #          "groupcode": 1
    #          }
    # header = {
    #     "token": res["token"]
    # }

    time.sleep(2)
    log_res = req.getCarryToken(log_url, data1)
    print(log_res)




