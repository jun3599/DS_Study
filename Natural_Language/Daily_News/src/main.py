from News_Data_Manager import * 
from text_analyzer_ver2 import * 
from text_manager import * 
import pandas as pd 


# # News = pd.read_excel('C://Users//wnsgn//Desktop//pro_git//data_science_study//DS_Study//ars_praxia_result.xlsx')

# # t = text_Analyzer(News, 'article')
# # t.draw_word_cloud()
# # t.latent_Dirichlet_allocation()
# # t.draw_n_nodes_network()


if __name__ == '__main__' :
    keyword = input("검색 키워드를 입력해주세요: ")
    N = Naver_News_Scrapper('C:/Users/wnsgn/Desktop/pro_git/data_science_study/DS_Study/Natural_Language/Daily_News/data')
    result = N.scrap_news(search_keywords=keyword)
    # t = text_Analyzer(result, 'article')
    # t.draw_word_cloud()
    # t.latent_Dirichlet_allocation()
    # t.draw_n_nodes_network()
    print(result)
    # result.to_excel('./test_scrap_0221.xlsx')

# # https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001
# 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=101&listType=paper&date=20220221'

import queue
from urllib.parse import quote 

# print(quote('list.naver?mode=LSD&mid=sec&sid1=101&listType=paper&date=20220221'))