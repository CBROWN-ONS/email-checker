from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from read_config import email

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://outlook.live.com/owa/")
browser.find_element(By.XPATH, '/html/body/header/div/aside/div/nav/ul/li[2]/a').click()
browser.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(email)
browser.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
time.sleep(5)

