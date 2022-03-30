from selenium import webdriver 
from scrapper_utils import * 

from bs4 import BeautifulSoup
import time 
import pandas as pd
import random
import multiprocessing as mp 



def get_news_contents(url):
        '''
        해당 함수에서는 url을 받아온 기사 하나에 대한 링크에 접근하고, 데이터를 추출하는 함수입니다.    
        [args]
        url : 대상 페이지의 url을 받아 동작합니다. 
        [Exception]
        '''
        # url접속 후 정보 수집 
        driver_loc = return_webdriver_location()
        options = initialize_options()
        driver = webdriver.Chrome(driver_loc, options=options)
        driver = fill_header(driver)

        driver.get(url)
        driver = fill_header(driver)
        driver.implicitly_wait(10)
        time.sleep(2)

        driver = scroll_down(driver)
        time.sleep(random.randint(1,3))
        raw = driver.page_source
        driver.quit()

        
        # 파싱 시작 
        soup = BeautifulSoup(raw, 'html.parser')

        try: 
            press = soup.find('div',{'class':'ofhd_float_head'}).find('h1',{'class':'ofhd_float_title'}).find('a').text

            try:
                category = soup.find('ul',{'class':'Nlnb_menu_list'}).find('li', {'class':'Nlist_item _LNB_ITEM is_active'}).find('span').text
            except:
                category = ''
            
            head = soup.find('div',{'class':'media_end_head go_trans'})
            
            try:
                reporter = head.find('div',{'class':'media_end_head_journalist'}).find('a').find('em').text
            except: 
                reporter = ''
            
            comment = head.find('div',{'class':'media_end_head_info_variety'}).find('div',{'class':'media_end_head_info_variety_left'}).find('div',{'class':'media_end_head_info_variety_cmtcount _COMMENT_HIDE'}).find('a').text
            
            recommend = soup.find('div',{'class':'ends_addition'}).find('div',{'class':'u_likeit_list_module _reactionModule'}).find('a').get_text()

            emotions = soup.find('div',{'class':'_reactionModule u_likeit'}).find('ul', {'class':'u_likeit_layer _faceLayer'})
            em_like = emotions.find('li',{'class':'u_likeit_list good'}).find('span',{'class':'u_likeit_list_count _count'}).get_text()
            em_warm = emotions.find('li',{'class':'u_likeit_list warm'}).find('span',{'class':'u_likeit_list_count _count'}).get_text()
            em_sad = emotions.find('li',{'class':'u_likeit_list sad'}).find('span',{'class':'u_likeit_list_count _count'}).get_text()
            em_angry = emotions.find('li',{'class':'u_likeit_list angry'}).find('span',{'class':'u_likeit_list_count _count'}).get_text()
            em_next = emotions.find('li',{'u_likeit_list want'}).find('span',{'class':'u_likeit_list_count _count'}).get_text()
        
        except:
            
            # 정상 접근은 성공했으나 파싱에 실패한 경우
            press = '파싱 실패'
            category = '파싱 실패'
            reporter = '파싱 실패'
            comment = '파싱 실패'
            recommend = '파싱 실패'
            em_like = '파싱 실패'
            em_warm = '파싱 실패'
            em_sad = '파싱 실패'
            em_angry = '파싱 실패'
            em_next = '파싱 실패'


        # 조회 결과를 모두 받아 데이터 프레임 생성 후 return 한다. 
        result = pd.DataFrame({'url':url, 'press': press, 'category':category, 'reporter':reporter, 'comment':comment, 'recommend':recommend, 'em_like':em_like, 'em_warm':em_warm, 'em_sad':em_sad, 'em_angry':em_angry, 'em_next':em_next} ,index=[0])        
        return result


def scrap_news(meta_df_info_dict):
        '''
        네이버 open api 를 활용해 뉴스 데이터를 스크랩핑합니다. 
        해당 함수에서는 get_news_meta_info 를 호출해 각각의 뉴스에 대한 메타 정보를 불러오고, 
        링크를 통해 각각의 계시물에 접근한 뒤, 뉴스의 컨텐츠를 조회해  데이터 프레임으로 반환합니다. 
        [args]
        [Exception]
        '''
        path = meta_df_info_dict['path']
        query_date = meta_df_info_dict['query_date']
        date = meta_df_info_dict['date']
        rank_type = meta_df_info_dict['rank_type']
        
        meta_df = pd.read_excel(path)
        
        urls = meta_df['url'].to_list()

        links = []
        for url in urls: 
            if pd.isna(url):
                pass 
            else: 
                links.append(url)
        
        # 빈 데이터 프레임을 만든다. 
        News = pd.DataFrame(columns=['url','press', 'category', 'reporter', 'comment', 'recommend', 'em_like', 'em_warm', 'em_sad', 'em_angry','em_next'])
        
        # 병렬처리 시작 
        MAX_PROCESS = mp.cpu_count()
        with mp.Pool(processes= MAX_PROCESS-2) as pool:
            # 각 프로세스에서 데이터 프레임을 생성한것을 return으로 받아 append해준다. 
            News = News.append(pool.map(func=get_news_contents, iterable=links), ignore_index=True)

        
        total = pd.merge(meta_df, News, how='left', on='url')
        
        file_path = 'C:/Users/wnsgn/Desktop/ars_praxia/news_scrapper/scr/Naver/result_data/data'
        file_name = f'/{rank_type}_Naver_{date}_{query_date}.xlsx'
        path = file_path+file_name

        total.to_excel(path, index=False)
        return None 

