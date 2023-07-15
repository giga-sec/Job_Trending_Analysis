import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import pyautogui
from random import randint


browser = webdriver.Chrome()
browser.switch_to.window(browser.current_window_handle)
time.sleep(2)
browser.maximize_window()
chrome_handle = pyautogui.getWindowsWithTitle("Google Chrome")[0]
pyautogui.switchToWindow(chrome_handle)

browser.get("https://accounts.google.com/signin")

time.sleep(10000)
