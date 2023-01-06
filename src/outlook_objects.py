from read_config import email
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re


class Email:
    def __init__(self, sender_name, sender_address, subject, content, element, browser):
        self.sender_name = sender_name
        self.sender_address = sender_address
        self.subject = subject
        self.content = content
        self.element = element
        self.browser = browser

    def flag_email(self):
        self.element.click()
        self.browser.find_element(By.XPATH, '//*[@id="innerRibbonContainer"]/div[3]/div/div/div/div[3]/div/div/span/button[1]/span').click()

    def delete_email(self):
        self.element.click()
        self.browser.find_element(By.XPATH, '//*[@id="id__246"]').click()

    def set_to_read(self):
        print(f"READING {self.subject} FROM {self.sender_address}")
        self.element.click()
        self.browser.find_element(By.XPATH, '//*[@id="id__225"]').click()


class Outlook:
    def __init__(self):
        self.browser = webdriver.Chrome()
        # TO BE REMOVED
        self.browser.maximize_window()
        self.loaded_mails = []
        self.inbox = []

    def login(self):
        self.browser.get("https://outlook.live.com/owa/")
        self.browser.find_element(By.XPATH, '/html/body/header/div/aside/div/nav/ul/li[2]/a').click()
        self.browser.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(email)
        self.browser.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()

        time.sleep(5)
        # if 'https://outlook.office365.com/mail/' == self.browser.current_url:
        #     pass
        # else:
        #     print("Invalid email - Please update the email in the config file")
        #     self.browser.close()
        #     self.browser = webdriver.Chrome()

    def get_emails(self, count=None, new_emails=False):
        page = self.browser.page_source
        soup = BeautifulSoup(page, 'html.parser')
        all_mails = soup.find_all('div', class_="hcptT")
        mail_elements = self.browser.find_elements(By.CLASS_NAME, "hcptT")
        for mail, el in zip(all_mails[0:count], mail_elements[0:count]):
            name_address = str(mail.find(class_="W3BHj gy2aJ Dc0o9 Ejrkd"))
            address, name = [str(x) for x in re.compile(r"title=.*?<").findall(name_address)[0].replace('"', '').replace('title=', '').strip('<').split('>')]
            content = str(soup.find('span', class_="FqgPc gy2aJ Ejrkd").text.strip('\n'))
            subject = str(soup.find('div', class_="IjzWp XG5Jd gy2aJ Ejrkd").text.strip('\n'))
            if new_emails:
                self.inbox.append(Email(name, address, subject, content, el, self.browser))
            else:
                self.loaded_mails.append(Email(name, address, subject, content, el, self.browser))

    def get_new_emails(self):
        self.browser.find_element(By.XPATH, '//*[@id="MainModule"]/div/div/div[3]/div/div[3]/div[1]/div[1]/div[1]/div/div[3]/div/div[1]/i/span/i').click()
        self.browser.find_element(By.XPATH, '//*[@id="fluent-default-layer-host"]/div[3]/div/div/div/div/div/div/ul/li[2]/button/div').click()
        self.get_emails(new_emails=True)
        time.sleep(5)
        self.browser.find_element(By.XPATH, '//*[@id="MainModule"]/div/div/div[3]/div/div[3]/div[1]/div[1]/div[1]/div/div[3]/div/div[1]').click()

    def get_loaded_emails(self):
        return self.loaded_mails

    def get_inbox(self):
        return self.inbox


out = Outlook()
out.login()
out.get_new_emails()
time.sleep(5)

