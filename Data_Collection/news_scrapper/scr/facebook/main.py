from account import *
from browser import * 
from facebook_parser import * 

# 계정 정보를 로드 합니다.
account_dict = return_account_info()

# 브라우징을 진행합니다. 
browser = facebook_browser(account_dict=account_dict)
info_dict = browser.browser(scroll_limit=200)

# 파싱을 진행합니다. 
facebook_parser(info_dict=info_dict, save_loc = 'C:/Users/wnsgn/Desktop/news_scrapper/facebook_news/data/data')
