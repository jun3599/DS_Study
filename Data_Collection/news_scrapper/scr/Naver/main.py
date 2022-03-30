from meta_scraper import *
from news_scraper import * 

if __name__ == '__main__':
    dates = ['20220302']
    m = meta_scraper(dates)
    result_dict = m.result_dict

    for key, info_dict in result_dict.items():
        scrap_news(info_dict)
