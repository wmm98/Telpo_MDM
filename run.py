"""
运行用例集：
    python3 run.py

# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'

"""

import sys
import pytest
from Common import Log
from Common import Shell
import subprocess
from Conf import Config
import os
import os.path
import time
import shutil
import datetime
from utils.base_web_driver import BaseWebDriver
from utils.client_connect import ClientConnect
from Common.check_yaml_file import CheckYaml
from Common.Serial import Serial
from Common.DealAlert import AlertData

if __name__ == '__main__':
    # init config file
    conf = Config.Config()
    conf.load_yaml_data()
    CheckYaml().check_test_data()
    test_info = conf.get_yaml_data()['MDMTestData']
    log = Log.MyLog()
    shell = Shell.Shell()

    # get COM port related
    usb_serial = Serial()
    usb_serial.get_current_COM()
    usb_serial.loginSer()
    usb_serial.confirm_relay_opened()

    # connect adb first
    device = ClientConnect()
    device.connect_device(test_info['android_device_info']['device_name'])
    # device.screen_keep_alive(test_info['android_device_info']['never_sleep_command'])
    # check current firmware version
    destination_version = test_info['ota_packages_info']['package_name'].split("-")[-1][:-4]
    current_firmware_version = shell.invoke("adb -s %s shell getprop ro.product.version" % test_info['android_device_info']['device_name'])
    alert_value = AlertData().get_yes_or_no("当前设备的固件为：%s,目标升级固件为：%s, 是否继续？" % (current_firmware_version, destination_version))
    if "否" in alert_value:
        sys.exit()
        # raise Exception("用户终止执行")
    AlertData().getAlert("请插上流量卡，请打开同一网段的wifi，茶上流量卡后请关掉弹框")

    log.info('initialize Config, path=' + conf.conf_path)
    # 先进行登录
    web = BaseWebDriver()
    # web.test_network_connection()
    url = test_info['website_info']['test_url']
    web.open_web_site(url)

    # 获取报告地址
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    pro_path = conf.project_path + "\\Report\\environment.properties"

    env_path = pro_path
    shutil.copy(env_path, xml_report_path)

    # # 定义测试集
    allure_list = '--allure-features=MDM_test02_login,MDM_usb-test1234'
    # allure_list = '--allure-stories=MDM_test02_login,MDM-Show'
    # pytest -s --allure-features pytest_debug
    # pytest -s --allure-features pytest_debug --allure-stories pytest_debug_story

    # 运行选中的case
    args = ['-s', '-q', '--ignore=system-warnings', '--alluredir', xml_report_path, allure_list]
    # args = ['-s', '-q', '--alluredir', xml_report_path, allure_list, allure_story]

    # 如下参数不添加allure_list，会自动运行项目里面带有feature监听器器的的所有case
    # args = ['-s', '-q', '--alluredir', xml_report_path]
    log.info('Execution Testcases List：%s' % allure_list)
    curr_time = datetime.datetime.now()
    log.info('Execution Testcases start time: %s' % curr_time)
    pytest.main(args)
    cmd = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)
    # 复制后的项目可手动清除或生成
    # allure generate xml -o html --clean

    try:
        shell.invoke(cmd)
    except Exception:
        log.error('@@@执行失败， 请检查环境配置！！！')
        raise
    # allure生成报表，并启动程序
    # subprocess.call(cmd, shell=True)
    # subprocess.call('allure open -h 127.0.0.1 -p 9999 ./report/html', shell=True)

    # 打开报告
    end_time = datetime.datetime.now()
    testpreiod = end_time - curr_time
    usb_serial.confirm_relay_closed()
    usb_serial.logoutSer()
    log.info('Execution Testcases End time: %s' % end_time)
    log.info('Execution Testcases total time: %s' % testpreiod)



