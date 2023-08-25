from selenium.common import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from datetime import datetime
from selenium.webdriver import Keys
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Conf.Config import Config
from Common.Log import MyLog
from System_Page import SystemPage
from Telpo_MDM_Page import TelpoMDMPage
from MDM_Page import MDMPage
from Base_Page import BasePage
from Devices_Page import DevicesPage
import time
import os
import re