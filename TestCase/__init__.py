from utils.base_web_driver import BaseWebDriver
from selenium.webdriver.support import expected_conditions as EC
from Page.MDM_Page import MDMPage
from Common.Log import MyLog
from Common import Log
from Page.OTA_Page import OTAPage
from Page.Devices_Page import DevicesPage
from Page.Message_Page import MessagePage
from Page.Telpo_MDM_Page import TelpoMDMPage
from Common.excel_data import ExcelData
from Conf.Config import Config
from Common.simply_case import Optimize_Case
from Common.DealAlert import AlertData
from Page.Release_Device_Page import ReleaseDevicePage
from Page.System_Page import SystemPage
from Page.Apps_Page import APPSPage
import time
from Page.Android_Aimdm_Page import AndroidAimdmPage
from utils.client_connect import ClientConnect

client = ClientConnect().get_device()
usb_device_info = {"device": client, "serial": client.serial}
# connect wifi adb
connect = ClientConnect()
connect.wifi_connect_device()
wifi_client = connect.get_wifi_device()
wifi_ip = connect.get_wifi_ip()
wifi_device_info = {"device": wifi_client, "ip": wifi_ip}
device_data = {"usb_device_info": usb_device_info, "wifi_device_info": wifi_device_info}



#
chrome_driver = BaseWebDriver()
test_driver = chrome_driver.get_web_driver()
