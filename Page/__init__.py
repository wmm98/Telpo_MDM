from selenium.common import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from datetime import datetime
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Conf.Config import Config
from Common.Log import MyLog
import time as t_time
import os
import re
from Common import Shell
import requests
from androguard.core.bytecodes.apk import APK
import uiautomator2 as u2
from uiautomator2.exceptions import UiaError
import allure
import hashlib
from PIL import Image
from Common.DealAlert import AlertData
import socket
from ping3 import ping
import threading
from bs4 import BeautifulSoup
# import warnings
from Common.Serial import Serial

yaml_data = Config().get_yaml_data()['MDMTestData']
# warnings.simplefilter('ignore', category=DeprecationWarning)


