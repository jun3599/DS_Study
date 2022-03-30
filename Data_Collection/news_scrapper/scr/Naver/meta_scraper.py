from datetime import datetime

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from scrapper_utils import * 
import random

from bs4 import BeautifulSoup 
import pandas as pd

class meta_scraper():
    def __init__(self, dates_list):
        '''
        입력한 일자의 기사 정보를 수집합니다. 
        [args]  
        dates_list: 수집 대상 일자의 리스트/ 각 일자 입력 형식: str -> yyyymmdd
        '''
        self.query_date = datetime.now()
        self.dates_list = dates_list
        self.result_dict = self.meta_parser()

        
    def meta_browser(self):

        dates = self.dates_list
        query_date = self.query_date.strftime('%Y%m%d')

        webdriver_loc = return_webdriver_location()
        options = initialize_options()

        driver = webdriver.Chrome(webdriver_loc, options=options)
        driver = fill_header(driver)
        # actions = ActionChains(driver=driver)

        v_url = 'https://news.naver.com/main/ranking/popularDay.naver'
        c_url = 'https://news.naver.com/main/ranking/popularMemo.naver'

        result_dict = {}
        for date in dates: 
            query = f'?date={date}'
            v_target = v_url + query
            c_target = c_url + query 

            print(v_target)  
            driver.get(v_target)
            driver = fill_header(driver)
            driver.implicitly_wait(10)
            time.sleep(random.randint(1,3))

            driver = scroll_down(driver)
            driver.implicitly_wait(10)
            v_source = driver.page_source

            v_raw_path = f'C:/Users/wnsgn/Desktop/ars_praxia/news_scrapper/scr/Naver/meta_data/raw/V_Naver_{date}_{query_date}.text'
            with open (v_raw_path, 'w',encoding= 'utf-8') as f:
                f.writelines(v_source)
            time.sleep(2)

            result_dict[f'V_meta_{date}'] = {'date':date, 'path': v_raw_path, 'rank_type':'V', 'query_date': query_date}

            print(c_target)  
            driver.get(c_target)
            driver = fill_header(driver)
            driver.implicitly_wait(10)
            time.sleep(random.randint(1,3))

            driver = scroll_down(driver)
            driver.implicitly_wait(10)
            c_source = driver.page_source

            c_raw_path = f'C:/Users/wnsgn/Desktop/ars_praxia/news_scrapper/scr/Naver/meta_data/raw/C_Naver_{date}_{query_date}.text'
            with open (c_raw_path, 'w',encoding= 'utf-8') as f:
                f.writelines(c_source)

            time.sleep(2)
            result_dict[f'C_meta_{date}'] = {'date': date, 'path': c_raw_path, 'rank_type':'C', 'query_date': query_date}

        driver.quit()

        return result_dict

    def meta_parser(self):
        result_dict = self.meta_browser()

        def parser(info_dict):
            date = info_dict['date']
            path = info_dict['path']
            rank_type = info_dict['rank_type']
            query_date = info_dict['query_date']

            # raw데이터 로드 
            with open(path, 'r', encoding='utf-8') as f: 
                raw = f.readlines()
            raw = str(raw)

            # soup 선언 
            soup = BeautifulSoup(raw, 'html.parser')

            # 컨텐츠 영역 확보 
            contents = soup.find_all('div',{'class':'rankingnews_box'})
            # 임시 데이터 프레임 생성 
            data = pd.DataFrame(columns=['press','rank','title','upload_date','url'])
            # 파싱 시작 
            for content in contents: 
                press = content.find('strong',{'class','rankingnews_name'}).text

                articles = content.find('ul',{'class':'rankingnews_list'}).find_all('li')
                for article in articles:
                    try:
                        rank = article.find('em').text
                        meta_info = article.find('div',{'class':'list_content'})
                        title = meta_info.find('a').text
                        url = meta_info.find('a')['href']
                        upload_date = article.find('span').text
                    except: 
                        rank = ''
                        title = ''
                        url = ''
                        upload_date = ''
                    
                    temp = {'date': date ,'press':press,'rank_type': rank_type,'rank':rank,'title':title,'upload_date':upload_date,'url':url}
                    data = data.append(temp, ignore_index=True)

            save_path = f'C:/Users/wnsgn/Desktop/ars_praxia/news_scrapper/scr/Naver/meta_data/data/{rank_type}_Naver_{date}_{query_date}.xlsx'
            data.to_excel(save_path,index=False)
            return save_path
        
        total_dict = {} 
        for key, info_dict in result_dict.items():
            date = info_dict['date']
            rank_type = info_dict['rank_type']
            query_date = info_dict['query_date']

            print(f'Meta: {key}에 대한 정보 파싱을 시작합니다.')
            path = parser(info_dict)

            total_dict[key] = {'date': date, 'path': path, 'rank_type': rank_type, 'query_date': query_date}
        
        return total_dict