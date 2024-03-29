import random
from bs4 import BeautifulSoup
import requests
# 쿼리어를 utf-8으로 인코딩 할때 사용합니다. 
from urllib.parse import quote
from pprint import pprint
import pandas as pd 

import time
from datetime import datetime 
import multiprocessing as mp 
# 네이버 개정정보를 반환하는 함수가 담긴 .py파일입니다. 
from NaverDevelopers_account import * 


class Naver_News_Scrapper():
    def __init__(self, path = 'C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\DS_Study\\Natural_Language\\Daily_News\\data'):
        '''
        클레스 초기화시, 수집될 데이터의 저장 경로(파일 위치)만 입력해주시면 됩니다. 
        만약 입력하지 않으면, 지정한 위치에 데이터가 수집됩니다. 
        '''
        self.path = path 
        self.results = {}
        
    def list_up_results(self):
        '''
        수집된 뉴스 데이터의 키워드 정보를 반환합니다. 
        '''
        print('총 수집된 뉴스 데이터의 키워드 정보: ', self.results.keys()) 
    
    def return_scrapped_data(self):
        if len(self.results.keys()) < 1:
            print('아직 수집된 데이터가 존재하지 않습니다.\n')
            return None 
        
        print('수집된 키워드 목록: ', self.list_up_results())
        keyword = input("조회를 원하는 키워드를 정확히 입력해주세요")
        if keyword not in self.results.keys():
            print('입력된 키워드에 대한 검색 정보가 존재하지 않습니다.')
            return None 
        return self.results[keyword]['data']
        
    def save_result(self, result, keywords, query_date):
        '''
        수집된 데이터를 저장하는 함수입니다.
        저장 위치 변경을 원하시면 
        '''
        file_name = f'{keywords}_{query_date}'
        file_path = f'{self.path}{file_name}.xlsx'
        result.to_excel(file_path)


    def get_news_meta_info(self, search_keywords, start=1, display=100, sort='date'):
        '''
        네이버 open api 이용해 뉴스 키워드 검색을 진행합니다. 
        뉴스 데이터를  불러옵니다. 
        [description]
        * 해당 방식으로 조회시, 해당 검색어에 대한 meta 정보만을 가져옵니다.                                              *
        * 따라서, 본문의 내용을 가져오기 위해서는 해당 정보에서 link를 조회해 저장하고, 이를 다시 검색하는 과정이 필요합니다. *
        * 해당 함수를 scrap_news 함수에 내장하여 자동적으로 결과를 조회하도록 구현합니다.                                    * 
        [args]
        header: Naver Dev.의 아이디와 페스워드를 dictionary형으로 전달합니다.  
        query: 검색 대상 키워드를 입력합니다. utf-8 변환은 함수 자체에서 처리합니다. 
        start: 검색 시작 인덱스입니다. 최소 1부터 최대 1000까지 가능합니다.  
        display: 검색 결과 출력 건 수를 의미합니다. 최소 10, 최대 100  
        sort: 정렬 옵션을 의미합니다. (sm: 유사도 순 | date: 날짜순(기본))
        '''
        # Naver Developers id와 비밀번호를 입력해 헤터를 생성해줍니다. 
        id, passwords = get_account_info()
        headers = {'X-Naver-Client-Id':id,
                'X-Naver-Client-Secret':passwords}
        
        # 쿼리할 url을 생성합니다. 
        keywords = quote(search_keywords, encoding='utf-8')
        # keywords = f'{keywords}&sm=tab_opt&sort=0&ds=2022.03.06&de=2022.03.06'

        # 반복문을 통해 1000까지 조회하면서 값을 추가합니다. 
        columns = ['description','link','originallink','pubDate','title']
        meta_info = pd.DataFrame(columns=columns)    
        
        # 루프 진행 
        start = 1 
        while start < 1000:
            url = 'https://openapi.naver.com/v1/search/news.json?query={}&start={}&display={}&sort={}&sm=tab_opt&sort=0&ds=2022.03.06&de=2022.03.06'.format(keywords,start,display,sort)

            # 검색 url과 유저정보를 담은 header을 입력하고 요청을 보냅니다. 
            res = requests.get(url, headers=headers)
            print(f"**{search_keywords}에 대한 검색어 조회 중, {start}번째 부터 {start+display}번째 검색 결과 조회중**")

            # 정상 접속 시 
            if res.status_code == 200:
                raw_json = res.json()
                # pprint(raw_json)
                info = pd.DataFrame(raw_json['items'])
                meta_info = meta_info.append(info, ignore_index=True)
                print("** 정상 처리 됌 ** ")
                time.sleep(1)
                
            # 비정상 접속 시 
            else: 
                print("!! 조회 에러 발생 !!")
                print("Error code: "+ str(res.status_code))
                pass 
            
            start = start + display
        
        return meta_info

    def return_parse_able_links(self, url_list):
        '''
        링크에 news.naver.com이 붙어있는 링크만을 걸러줍니다.
        '''
        result = []
        for link in url_list:
            if 'news.naver.com' not in link:
                pass 
            else:
                result.append(link)
        return result

    def get_news_contents(self, url):
        '''
        네이버 open api 를 활용해 뉴스 데이터를 스크랩핑합니다. 
        해당 함수에서는 url을 받아온 기사 하나에 대한 링크에 접근하고, 데이터를 추출하는 함수입니다.   
        이 함수는 scrap_news함수에서 처리해 전체 데이터를 수집하는데 이용됩니다.  
        [args]
        url : 대상 페이지의 url을 받아 동작합니다. 
        [Exception]
        '''
        useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        ,'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        ,'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36']

        header = {"User-Agent":useragents[random.randint(0,2)]}
        
        res = requests.get(url, headers=header)
        time.sleep(3)
        # 정상 조회시 
        if res.status_code == 200:
            if 'news.naver.com' not in res.url:
                print(f"{url}은 파싱할 수 없는 페이지입니다.")
                return None 

            try:
                # 파싱 시작 
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # 기사 정보 영역 조회 
                article_info = soup.find("div",{"class":"article_info"})
                
                # 기사 제목 조회 
                title = article_info.find('h3',{'id':'articleTitle'}).text
                # 기사 입력 일자 조회 
                input_date = article_info.find('span',{'class':'t11'}).text
                
                # 본문 내용 전체 조회 
                article = soup.find('div',{'class': "_article_body_contents article_body_contents"}).text
                
                # 조회 결과를 모두 받아 데이터 프레임 생성 후 return 한다. 
                result = pd.DataFrame({'title':title, 'input_date':input_date, 'article': article} ,index=[0])
                print(f'ㅎㅎ{url} 정상 파싱 완료!! ')
                return result

            except:
                # 정상 접근은 성공했으나 파싱에 실패한 경우
                print(f"! {url} 파싱 실패")
                
        else: 
            # 접속에 문제가 발생한 경우 
            print(f"! {url} 접근 실패")
        

    def scrap_news(self, search_keywords, start=1, display=100, sort='date'):
        '''
        네이버 open api 를 활용해 뉴스 데이터를 스크랩핑합니다. 
        해당 함수에서는 get_news_meta_info 를 호출해 각각의 뉴스에 대한 메타 정보를 불러오고, 
        링크를 통해 각각의 계시물에 접근한 뒤, 뉴스의 컨텐츠를 조회해  데이터 프레임으로 반환합니다. 
        [args]
        [Exception]

        '''
        query_date = datetime.now().strftime("%Y%m%d_%H%M")   
        meta_info = self.get_news_meta_info(search_keywords, start, display, sort)
        # 링크만 리스트로 만들어 return_parse_able_links를 호출합니다. 
        # 결과로써, 파싱 가능한 링크만을 담아옵니다. 
        links = list(meta_info['link']) 
        links = self.return_parse_able_links(links)

        # 빈 데이터 프레임을 만든다. 
        News = pd.DataFrame(columns=['title','input_date','article'])
        # 병렬처리 시작 
        MAX_PROCESS = mp.cpu_count()
        with mp.Pool(processes= MAX_PROCESS) as pool:
            # 각 프로세스에서 데이터 프레임을 생성한것을 return으로 받아 append해준다. 
            News = News.append(pool.map(func=self.get_news_contents, iterable=links), ignore_index=True)
        
        self.results[search_keywords] = {'data':News, 'query_date': query_date}

        save_option = input("수집된 정보를 저장하시겠습니까? (y/n) ")
        if save_option == 'y':
            self.save_result(News, search_keywords, query_date)
        else: 
            print("파일을 저장하지 않습니다.")

        return News
