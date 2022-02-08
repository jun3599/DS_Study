from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from customer_email import customer_info_management
from contents import *

import time
import sys 

from selenium.webdriver.firefox import firefox_profile



class auto_mail:
    def __init__(self,url='https://google.com'):
        self.Table_manager = customer_info_management('C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\Web_Scraper_and_Use_API\\selenium_tutorials\\exam_mail\\customer_info.xlsx')
        self.Table = self.Table_manager.load_Table()

        self.title , self.contents = load_contents()
        
        self.url = url 
        self.driver = webdriver.Chrome('C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\Web_Scraper_and_Use_API\\selenium_tutorials\\chromedriver.exe')
        self.driver.get(self.url)
        self.action = ActionChains(self.driver)
        self.driver.maximize_window()
        time.sleep(2)

    def login(self,id,password):
        self.driver.find_element_by_css_selector('.gb_1.gb_2.gb_1d.gb_1c').click()
        self.action.send_keys(id).pause(1).send_keys(Keys.ENTER).perform()
        self.action.reset_actions()
        time.sleep(2)

        self.action.send_keys(password).send_keys(Keys.ENTER).perform()
        self.action.reset_actions()
        time.sleep(2)


    
    def send_mail(self, option=0):        

        # option 0: 등록된 모든 사용자에게 메일 
        if option == 0:
            target_user = self.Table

        # 입력한 특정 사용자에게만 전달 
        elif option == 1:
            print(self.Table)
            target_user_list = list(map(str, input("발송하고자 하는 고객의 id를 입력해주세요 (구분자: \' \')\n").split(' ')))
            target_user = self.Table_manager.query_info(target_user_list)

        # 특정 사용자만 제외하고
        elif option == 2:
            print(self.Table)
            except_users = list(map(str, input("제외할 대상의 id값을 입력하세요(\' \'로 구분)").split(' ')))
            all_users = self.Table['id'].to_list()
            target_user_list = [x for x in all_users if x not in except_users]
            target_user = self.Table_manager.query_info(target_user_list)

        target_addresses = target_user['email'].to_list()
        
        
        
        self.driver.get('https://mail.google.com/')
        time.sleep(3)
        
        self.driver.find_element_by_css_selector('.T-I.T-I-KE.L3').click()
        time.sleep(2)

        send_btn = self.driver.find_element_by_css_selector('.gU.Up')

        for em in target_addresses:
            self.action.send_keys(em).key_down(Keys.TAB)
        self.action.reset_actions

        (
            self.action.key_down(Keys.TAB)
            .send_keys(self.title).pause(1)
            .key_down(Keys.TAB)
            .send_keys(self.contents).pause(2)
            .move_to_element(send_btn).click().perform()
        )

        self.action.reset_actions()



