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

#
chrome_driver = BaseWebDriver()
test_driver = chrome_driver.get_web_driver()
# EC = EC
# MDMPage = MDMPage
# MyLog = MyLog
# Log = Log
# OTAPage = OTAPage
# DevicesPage = DevicesPage
# MessagePage = MessagePage
# TelpoMDMPage = TelpoMDMPage
# ExcelData = ExcelData
# Config = Config
# Optimize_Case = Optimize_Case
# AlertData = AlertData
# ReleaseDevicePage = ReleaseDevicePage
# SystemPage = SystemPage
# APPSPage = APPSPage
# time = time