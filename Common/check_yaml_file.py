from Conf.Config import Config
import os
conf = Config()

conf.load_yaml_data()
yaml_data = conf.get_yaml_data()['MDMTestData']


class CheckYaml:
    def __init__(self):
        self.value_not_existed = []
        self.err_meg_list = []

    def check_test_data(self):
        self.check_value_existed(yaml_data["website_info"])
        self.check_value_existed(yaml_data["app_info"])
        self.check_value_existed(yaml_data["ota_packages_info"])
        self.check_value_existed(yaml_data["android_device_info"])
        self.check_value_existed(yaml_data["work_app"])
        self.check_value_existed(yaml_data["system_app"])

        self.check_file_existed(yaml_data["system_app"], "Package")
        self.check_file_existed(yaml_data["work_app"], "Work_APP")
        self.check_file_existed(yaml_data["app_info"], "Package")
        self.check_file_existed(yaml_data["ota_packages_info"], "Package")
        self.check_file_existed(yaml_data["Content_info"], "Content")

        flag = 0
        if len(self.value_not_existed) > 0:
            flag += 1
            for none_msg in self.value_not_existed:
                print(none_msg)

        if len(self.err_meg_list) > 0:
            flag += 1
            for err_msg in self.err_meg_list:
                print(err_msg)
        if flag > 0:
            yaml_path = conf.project_path+"\\Config\\test_data.yaml"
            raise Exception("@@@请检查%s里面的数据" % yaml_path)

    def check_value_existed(self, data, dict_=True):
        if not dict_:
            if not data:
                msg = "%s的值为空, 请检查！！！！" % data
                self.value_not_existed.append(msg)
        else:
            for key in data:
                if not data[key]:
                    msg = "%s的值为空, 请检查！！！！" % key
                    self.value_not_existed.append(msg)

    def check_file_existed(self, data, directory, dict_=True):
        dir_path = conf.project_path + "\\Param\\%s" % directory
        if not dict_:
            if "." in data:
                file_path = "%s\\%s" % (dir_path, data)
                if not os.path.exists(file_path):
                    msg = "%s不存在, 请检查！！！" % file_path
                    self.err_meg_list.append(msg)
        else:
            for key in data:
                if data[key] is not None:
                    if isinstance(data[key], list):
                        for i in data[key]:
                            file_path = "%s\\%s" % (dir_path, i)
                            if not os.path.exists(file_path):
                                msg = "%s不存在, 请检查！！！" % file_path
                                self.err_meg_list.append(msg)
                    else:
                        if "." in data[key]:
                            file_path = "%s\\%s" % (dir_path, data[key])
                            if not os.path.exists(file_path):
                                msg = "%s不存在, 请检查！！！" % file_path
                                self.err_meg_list.append(msg)


if __name__ == '__main__':
    test = CheckYaml()
    conf.load_yaml_data()
    test.check_test_data()
















