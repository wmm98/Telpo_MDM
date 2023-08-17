import requests


class RequestMethodCarryFormData:
    """
    定义请求类型
    以表单方式form-data传递参数
    """

    def __init__(self):

        """初始化参数"""
        self.data = {}
        self.files = {}

    def get(self, url, data, headers):
        """
        定义get方法请求
        :return:
        """
        try:
            return requests.get(url=url, data=data, headers=headers, timeout=60)
        except TimeoutError:
            return print('%s get request timeout!' % url)

    def getCarryToken(self, url, data, headers):
        """
        定义get方法请求，额外添加token
        :return:
        """
        try:
            return requests.get(url=url, json=data, headers=headers, timeout=60)
        except TimeoutError:
            return print('%s get request timeout!' % url)

    def post(self, url, data, headers):
        """
        定义post方法请求
        这个携带json应该不需要额外改
        :return:
        """
        try:
            return requests.post(url=url, data=data, headers=headers, timeout=60)
        except TimeoutError:
            return print('%s post request timeout!' % url)
