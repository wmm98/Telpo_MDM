from configparser import ConfigParser
from Common import Log
import os


class Config():
    TITLE_RELEASE = "online_release"
    VALUE_CASES_PATH = "cases_path"

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = Log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.xml_report_path = Config.path_dir + '/Report/xml'
        self.html_report_path = Config.path_dir + '/Report/html'
        # print(self.xml_report_path, self.xml_report_path)
        self.log_path = Config.path_dir + '/Log'
        self.project_path = Config.path_dir

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path, encoding='utf-8-sig')
        # self.tester_release = self.getConf(Config.TITLE_RELEASE, Config.VALUE_TESTER)
        # self.environment_release = self.getConf(Config.TITLE_RELEASE, Config.VALUE_ENVIRONMENT)
        self.cases_path = self.getConf(Config.TITLE_RELEASE, Config.VALUE_CASES_PATH)
        # print(self.cases_path)
        self.CN_input_method = ["com.sohu.inputmethod.sogou/.SogouIME", "com.google.android.inputmethod.pinyin/.PinyinIME", "com.android.inputmethod.pinyin /.PinyinIME"]

    def getConf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

if __name__ == '__main__':
    conf = Config()
    print(conf.project_path)