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

    def get(self, url, data):
        """
        定义get方法请求
        :return:
        """
        try:
            res = requests.get(url=url, params=data, headers=self.header, timeout=60)
            return res.json()
        except TimeoutError:
            return print('%s get request timeout!' % url)

    def getCarryToken(self, url, data):
        """
        定义get方法请求，额外添加token
        :return:
        """
        try:
            res = requests.get(url=url, params=data, headers=self.header, timeout=60)
            print(res.content)
            return res.json()
        except TimeoutError:
            return print('%s get request timeout!' % url)

    def postCarryToken(self, url, data):
        """
        定义post方法请求
        这个携带json应该不需要额外改
        :return:
        """
        try:
            res = requests.post(url=url, data=data, headers=self.header, timeout=60)
            print(res.content)
            return res.json()
        except TimeoutError:
            return print('%s post request timeout!' % url)

    def post(self, url, data):
        try:
            res = requests.post(url=url, data=data, timeout=60)
            self.token = res.json()["token"]
            self.header["token"] = self.token
            return res.json()
        except TimeoutError:
            return print('%s post request timeout!' % url)


if __name__ == '__main__':
    url = "http://test.telpopaas.com/login"
    data = {
        "account": "ceshibu",
        "password": "123456",
        "platform": "mdm"
    }
    # req = RequestMethodCarryFormData()
    res = requests.post(url, data).json()
    print(res)
    # print(type(res))
    # time.sleep(5)
    log_url = "http://test.telpopaas.com/appLogs"
    # log_url = "http://test.telpopaas.com/caculateAppLogs"
    data1 = {"page": 1, "offset": 30}
    # data1 = {"page": 1,
    #          "offset": 5,
    #          "share": 0,
    #          "verifyed": 0,
    #          "groupcode": 1
    #          }
    header = {
        "token": res["token"]
    }

    # header = {: }
    # log_res = req.getCarryToken(log_url, data1)
    log_res = requests.get(url=log_url, params=data1, headers=header)
    print(log_res.content)




