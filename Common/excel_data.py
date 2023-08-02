import xlrd
from Conf.Config import Config
from Common import Log

log = Log.MyLog()

conf = Config()


class ExcelData:
    def __init__(self):
        pass

    def get_template_data(self, path, sheet):
        self.file = xlrd.open_workbook(path)
        self.sheet1 = self.file.sheet_by_name(sheet)
        dataresult = []
        result = []
        for i in range(1, self.sheet1.nrows):
            if len(self.sheet1.row_values(i)[0]) == 0 or len(self.sheet1.row_values(i)[1]) == 0:
                err = "@@@ %s 数据有空缺， 请检查！！！" % sheet
                print(err)
                log.error(err)
                raise Exception
            dataresult.append(self.sheet1.row_values(i))
        dataresult.insert(0, self.sheet1.row_values(0))

        for i in range(1, len(dataresult)):
            temp = dict(zip(dataresult[0], dataresult[i]))
            result.append(temp)
        return result


if __name__ == '__main__':
    path = conf.project_path + "\\Param\\device import.xlsx"
    data = ExcelData()
    # devices_list = data.get_template_data(path, "devices")
    # print(devices_list)

    cate_model_list = data.get_template_data(path, "cate_model")
    print(cate_model_list)
