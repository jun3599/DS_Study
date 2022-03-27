from selenium import webdriver 
from selenium.webdriver import ActionChains 
from selenium.webdriver.common.keys import Keys 

from urllib.parse import quote 
from scrapper_utils import * 

from account import * 

import time
import random 


url = 'https://www.facebook.com/'
keyword = input("검색어를 입력해주세요: ")
login_info = return_account_info()

driver_loc = return_webdriver_location()
options = initialize_options()

driver = webdriver.Chrome(executable_path=driver_loc, options=options)
driver = fill_header(driver)
actions = ActionChains(driver)

driver.get(url)
driver.implicitly_wait(20)
time.sleep(random.randint(2,5))
driver = deal_with_modal_popup(driver)

# 로그인 파트
# driver.find_element_by_xpath('//*[@id="u_0_a_qN"]/div[1]/div[1]').click()
actions.send_keys(login_info["ID"]).pause(random.randint(1,2)).key_down(Keys.TAB).send_keys(login_info["PW"]).pause(random.randint(2,3)).key_down(Keys.TAB).perform()
actions.reset_actions()
driver.find_element_by_name("login").click()
driver = fill_header(driver)
driver.implicitly_wait(12)
time.sleep(5)
driver = deal_with_modal_popup(driver)

# 검색 시작 
driver = deal_with_modal_popup(driver)
# driver = del_popups(driver)
# driver.find_element_by_css_selector('#mount_0_0_0K > div > div:nth-child(1) > div > div:nth-child(4) > div.rq0escxv.byvelhso.q10oee1b.poy2od1o.j9ispegn.kr520xx4.ooia0uwo.kavbgo14.mhnrfdw6 > div > div > div > div > div > label > input').click()
# time.sleep(random.randint(1,3))
# actions.send_keys(keyword).pause(2).ket_down(Keys.ENTER).perform()
# actions.reset_actions()
keyword = quote(keyword,encoding='utf-8')
driver.get(f'https://www.facebook.com/search/top/?q={keyword}')
driver = fill_header(driver)
driver.implicitly_wait(20)
time.sleep(2)

# 스크롤링 
driver = deal_with_modal_popup(driver)
driver = scroll_down(driver)
time.sleep(3)

# 페이지 소싱
driver = deal_with_modal_popup(driver) 
raw_data = driver.page_source
driver.quit()

with open('./test.text', 'w') as f:
    f.writelines(raw_data)
