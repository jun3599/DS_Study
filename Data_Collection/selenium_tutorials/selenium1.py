from selenium import webdriver
# chrome 버전과 chrome driver 의 버전 일치 여부는 반드시 확인해야 합니당~ 
# 흔히 사용되는 키들을 미리 가져옵니다.(엔터, 클릭 등등)
from selenium.webdriver.common.keys import Keys 

# 1. 웹드라이버 객체를 열어줍니다. 
# 만약 chromdriver를 같은 경로에 넣어주지 않았다면, 밑의 드라이버 객체에서 경로를 알려줘야 합니다.
# driver = webdriver.Chrome('C:\\Users\wnsgn\\Desktop\\pro_git\\data_science_study\Web_Scraper_and_Use_API\\selenium_tutorials\\chromedriver.exe')
driver = webdriver.Chrome()

# 2. 드라이버를 통해 일단 구글을 열어줍니다. 
link = "https://google.com"
driver.get(link)

# 기본적으로, 드라이버가 웹 상의 특정 위치에서의 원소를 조회하고 입력하는 동작은 html테그를 활용해 접근합니다. 

# 3. 검색창을 이용합니다. 
# 검색창의 테그 정보중 class="gLFyf gsfi"를 활용합니다. 
# 드라이버를 통해 class="gLFyf gsfi"테그를 찾고, --> send_keys를 통해 입력 
# css이기 때문에 가장 앞에 . & 공백도 .으로 채워줍니다.
driver.find_element_by_css_selector(".gLFyf.gsfi").send_keys('파이썬')
# 검색 버튼을 누르거나 엔터를 눌러 검색 (여기서는 엔터로)
driver.find_element_by_css_selector(".gLFyf.gsfi").send_keys(Keys.ENTER)


# 4. 검색결과에서 특정 게시물을 클릭합니다. 
# 모든 게시물은 class="LC20lb MBeuO DKV0Md" 를 가집니다.

# 별도의 설정이 없다면 첫번째 게시글을 가져옵니다. 
# driver.find_element_by_css_selector('.LC20lb.MBeuO.DKV0Md').click()

# 두번째 혹은 다른 순서것을 누르고 싶다면
# 1) elenment --> elements 
# 2) 가져온 것을 배열처럼 접근 후 클릭
driver.find_elements_by_css_selector('.LC20lb.MBeuO.DKV0Md')[1].click()

