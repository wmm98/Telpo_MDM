import shutil
import datetime
from Common import Shell
from Conf.Config import Config
import pytest
from Common import Log
from Common.check_yaml_file import CheckYaml
from utils.base_web_driver import BaseWebDriver
from Common.Get_Lan_ips import GetLanIps
import Stability_Cases as st


if __name__ == '__main__':
    # init config file
    lan = GetLanIps()
    conf = Config()
    conf.load_yaml_data()
    CheckYaml().check_test_data()
    test_info = conf.get_yaml_data()['MDMTestData']
    log = Log.MyLog()

    # 获取局域网下所有的ip
    st.lan_ips.start_thread()

    # 先连接adb
    # device.wifi_connect_device()
    # device.connect_device(test_info['android_device_info']['device_name'])
    # device.screen_keep_alive(test_info['android_device_info']['never_sleep_command'])

    shell = Shell.Shell()

    log.info('initialize Config, path=' + conf.conf_path)
    # 先进行登录
    web = BaseWebDriver()
    web.open_web_site(test_info['website_info']['test_url'])

    # 获取报告地址
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    pro_path = conf.project_path + "\\Report\\environment.properties"

    env_path = pro_path
    shutil.copy(env_path, xml_report_path)

    # # 定义测试集
    allure_list = '--allure-features=MDM_stability,MDM_stability_test1111'
    # allure_story = '--allure-stories=pytest_debug_story'
    # pytest -s --allure-features pytest_debug
    # pytest -s --allure-features pytest_debug --allure-stories pytest_debug_story

    # 运行选中的case
    args = ['-s', '-q', '--alluredir', xml_report_path, allure_list]
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
    print(end_time)
    testpreiod = end_time - curr_time
    print(testpreiod)
    log.info('Execution Testcases End time: %s' % end_time)
    log.info('Execution Testcases total time: %s' % testpreiod)
