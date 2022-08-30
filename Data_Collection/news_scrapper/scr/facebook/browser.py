from selenium import webdriver 
from selenium.webdriver import ActionChains 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By

from urllib.parse import quote 
from scrapper_utils import * 

from account import * 

import time
import random 
from datetime import datetime 

# print(datetime.now().strftime('%Y%m%d %H:%M:%S'))

class facebook_browser():
    def __init__(self, account_dict):

        self.account_dict = account_dict 
        self.choose_target()
        self.query_date = datetime.now()
        self.query_date_str = self.query_date.strftime('%Y%m%d')

    def choose_target(self):
        '''
        클래스 선언 초기에 사용되며,
        입력값에 따라 수집 대상 사이트를 선정합니다. 
        [args]
        none 
        
        [return]
        str: 대상 사이트 url명칭
        '''
        selected = input("수집을 원하시는 사이트의 번호를 입력해주세요\n(1: 조선일보, 2: 중앙일보, 3: 동아일보)")
        
        if selected == '1':
            target_site = 'chosun' 
        elif selected == '2':    
            target_site = 'joongang'
        elif selected == '3':
            target_site = 'dongamedia'
        
        self.target_site = target_site
    
    def save_raw(self, raw_data, save_path = 'C:/Users/wnsgn/Desktop/news_scrapper/facebook_news/data/raw'):        
        '''
        수집된 원자료를 저장하고 경로를 반환합니다. 
        [args]
        raw_data: 수집된 원자료(html문서) 
        save_path: 파일이 저장될 절대 경로
        [return]
        path: 파일이 저장된 경로 및 파일 이름 
        '''
        file_name = f'/{self.target_site}_{self.query_date_str}'
        path = save_path + file_name
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(raw_data) 

        return path 
    
    def browser(self, scroll_limit= 100): 
        '''
        실제 페이지 브라우징을 진행하는 함수입니다.   
        페이스북에 접속 후, 로그인을 진행한 뒤, 타겟 사이트에 접근합니다.   
  
        타겟으로 선정된 페이지에 접속 후, 스크롤을 입력한 횟수만큼 진행하고,   
        페이지의 html 정보를 수집후 이를 저장하고 프로그램을 종료합니다.   
        [args]  
        scroll_limit: 최대 스크롤 횟수를 지정합니다.   
        [return]  
        info_dict: parser에게 전달할 정보 딕셔너리입니다.   
            - path: 파일 저장 경로입니다.  
            - date: 데이터 조회 시점입니다.  
            - site: 조회 대상 계정 이름입니다. 
        '''
        url = 'https://www.facebook.com/'
        # target_site = 'chosun' 
        target_site = self.target_site

        # 계정 정보 로드 
        login_info = self.account_dict

        # 드라이버 옵션 초기화 
        driver_loc = return_webdriver_location()
        options = initialize_options()
        driver = webdriver.Chrome(executable_path=driver_loc, options=options)
        driver = fill_header(driver)
        actions = ActionChains(driver)

        # 초기 화면 접근 
        driver.get(url)
        driver = fill_header(driver)
        driver.implicitly_wait(20)
        time.sleep(random.randint(2,5))
        driver = deal_with_modal_popup(driver)

        # 로그인 파트
        actions.send_keys(login_info["ID"]).pause(random.randint(1,2)).key_down(Keys.TAB).send_keys(login_info["PW"]).pause(random.randint(2,3)).key_down(Keys.TAB).perform()
        actions.reset_actions()
        driver.find_element_by_name("login").click()
        driver = fill_header(driver)
        driver.implicitly_wait(12)
        time.sleep(5)
        driver = deal_with_modal_popup(driver)

        # 검색 시작 
        driver = deal_with_modal_popup(driver)
        driver.get(url+target_site)
        driver = fill_header(driver)
        driver.implicitly_wait(20)
        time.sleep(2)

        # 스크롤링 
        driver = deal_with_modal_popup(driver)
        driver = scroll_down(driver,scroll_limit= scroll_limit)
        time.sleep(3)


        # 페이지 소싱
        driver = deal_with_modal_popup(driver) 
        raw_data = driver.page_source
        driver.quit()

        path = self.save_raw(raw_data, save_path = 'C:/Users/wnsgn/Desktop/news_scrapper/facebook_news/data/raw')

        info_dict = {'path': path, 'date':self.query_date, 'site': self.target_site}
        return info_dict

# def save_raw(filepath='', ): 

# def facebook_browser():
