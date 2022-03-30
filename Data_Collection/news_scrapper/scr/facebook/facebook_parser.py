from bs4 import BeautifulSoup 
import pandas as pd 
import re 

from datetime import datetime 

def facebook_parser(info_dict, save_loc = 'C:/Users/wnsgn/Desktop/news_scrapper/facebook_news/data/data'):
    '''
    브라우저를 통해 추출한 raw data를 파싱합니다.    
    파싱된 데이터는 엑셀에 저장후 프로그램을 종료합니다.   
      
    [args]
    info_dict: 브라우징의 결과로 리턴된 정보 딕셔너리입니다.
    save_loc: 파싱된 결과를 저장할 위치입니다.   
    [return]  
    None : 데이터를 저장후 리턴값 없이 종료됩니다. 
    '''
    # 브라우징 정보 확인 
    raw_data_path = info_dict['path']
    query_date = info_dict['date']
    site = info_dict['site']

    # 원 자료 로드 
    with open(raw_data_path, 'r', encoding='utf-8') as f:
        raw = f.readlines()
    raw = str(raw)

    # 파싱 시작 선언 
    soup = BeautifulSoup(raw, 'html.parser')
    # 최종 반환 데이터프레임 초기화 
    data = pd.DataFrame(columns=['조회일자','게시일자', '게시글본문', '기사제목', '기사설명', 'url','댓글_공유', '공감수'])
    
    # 콘턴츠 영역 전체 수집  
    contents = soup.find_all('div', {'class':'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'})
    # 콘텐츠별 정보 수집 
    for content in contents: 
        조회일자 = query_date
        게시일자 = content.find('a',{'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw'}).text
        게시일자 = re.sub('=','',게시일자) 
        
        try: 
            게시글본문 = content.find('span',{'class':'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m'}).get_text()
        except:
            게시글본문 = ''
        try: 
            main = content.find('div',{'class':'stjgntxs ni8dbmo4'})
            기사제목 = main.find('span',{'class':'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ojkyduve'}).text
            기사설명 = main.find('span',{'class':'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5'}).text
            url = main.find('a',{'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 a8c37x1j p8dawk7l'})['href']
        except: 
            기사제목 = ''
            기사설명 = ''
            url = ''
        
        referral_info_area = content.find('div',{'class':'l9j0dhe7'})
        공감수 = referral_info_area.find('span',{'class':'pcp91wgn'}).text

        댓글_공유 = referral_info_area.find('div',{'class':'bp9cbjyn j83agx80 pfnyh3mw p1ueia1e'}).text

        temp = {'조회일자':조회일자 ,'게시일자':게시일자, '게시글본문':게시글본문, '기사제목':기사제목, '기사설명':기사설명, 'url':url, '공감수':공감수, '댓글_공유':댓글_공유}
        data = data.append(temp, ignore_index=True)

    # 파일 이름 및 저장 경로 지정 
    query_date = query_date.strftime('%Y%m%d')
    file_name = f'/{site}_{query_date}.xlsx'
    path = save_loc + file_name

    data.to_excel(path, index=False)
    
