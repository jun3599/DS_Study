# 강의2 : 셀레니움의 webdriver와 actionchains를 사용하여 구글 지메일을 자동으로 발송 
# 웹사이트 자동화의 근본. 
# 셀레니움은 웹페이지 자동화 뿐 아닌 크롤링 프로그램으로도 작동 가능하기 때문에 유용 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
# 새로 사용하는 도구
from selenium.webdriver.common.action_chains import ActionChains
# 시간에 따라 이메일을 보낼때 사용
import time 

#0. 드라이버 객체 생성 후 페이지 열기 까지
driver = webdriver.Chrome()
url = 'https://google.com'
driver.get(url)
# 창 최대크기로 
driver.maximize_window()
time.sleep(2)
# 0-2 : action chain 생성 
# actionchain기능은 여러개의 동작을 체인으로 엮어 저장하고 실행하는 기능 
# 복잡하고 자주 쓰이는 일련의 동작을 엮어줌으로써 재활용성을 높여줍니다. 
#   1) actionchain 객체 생성 
#   2) 객체.perform()으로 실행 
action = ActionChains(driver) # 드라이버의 권한을 넘겨주는 모습

# 1. 우선 로그인 창으로 이동
# class="gb_3 gb_4 gb_3d gb_3c"
# driver.find_element_by_css_selector('???') 을 사용시 id를 통해 접근 시 #을 class를 통해 접근시 .을 이용
driver.find_element_by_css_selector('.gb_1.gb_2.gb_1d.gb_1c').click()
# 1-1 ) 아이디 입력시 해당영역의 html 테그를 찾아 입력하는 방식도 있지만, 별달리 동작을 입력하지 않아도 
#       바로 키를 입력할 수 있다면 딱히 해당 테그를 찾을 필요가 없다 --> 이때, actionchain 사용 
# action.send_keys('wnsgnl8229@gmail.com').send_keys(Keys.ENTER).perform() # 다만 실행 메서드 꼭 입력 .perform()
action.send_keys('junny3599@gmail.com').perform() # 다만 실행 메서드 꼭 입력 .perform()
action.reset_actions() # 엑션을 여러번 만들고 사용할 때 에러를 방지 : 엑션의 내용을 초기화 
driver.find_element_by_css_selector(".VfPpkd-vQzf8d").click()
time.sleep(2)

action.send_keys('gkwlak1!').pause(2).send_keys(Keys.ENTER).perform()
action.reset_actions()
time.sleep(3)

#2. gmail 이동 
# gmail 이동 클레스 class="gb_f"
# driver.find_element_by_css_selector('???') 을 사용시 id를 통해 접근 시 #을 class를 통해 접근시 .을 이용
# driver.find_element_by_css_selector('.gb_f').click()
driver.get('https://mail.google.com/')
time.sleep(3)


# 3. 메일 쓰기 

# 3-1) 메일 쓰기 버튼 위로 마우스(?) 이동 --> 클릭 키 다운  
# 해당위치를 변수로 다룰 수 있음을 보여줄 뿐 
#  사실 이렇게 도 가능 : driver.find_element_by_css_selector('???').clock()
write_btn = driver.find_element_by_css_selector('.T-I.T-I-KE.L3')
action.move_to_element(write_btn).click().perform()
action.reset_actions()
time.sleep(2)

# 3-2) 메일 내용 쓰기 :: 받는사람 + 제목 + 내용
## 꿀팁 : tap 누르면 다음 내용 작성란으로 이동 한다 
# 따라서 action chain을 사용해 넘어가는 방식으로 진행한다. 
# 이번 실습을 끝내고 대량 메일 발송 예제를 진행해보자! 
# 조금 긴 acrion chain을 사용할 때에는 pause(sec)을 사용해 의도적인 스탑을 걸어준다. 
send_btn = driver.find_element_by_css_selector('.gU.Up')

(
    action.send_keys("junny3599@gmail.com").pause(1)
    .key_down(Keys.TAB).key_down(Keys.TAB)
    .send_keys("안녕하세요 박준휘 입니다. selenium을 통한 자동화 메일 테스트 입니다.").pause(1)
    .key_down(Keys.TAB)
    .send_keys("어그로 끌어서 죄송함당!\n 추운 겨울 모쪼록 좋은 날들 보내시고\n").key_down(Keys.SHIFT).send_keys('covid').key_up(Keys.SHIFT).send_keys('-19 조심하세요!').pause(1)
    .move_to_element(send_btn).click().perform()
)

action.reset_actions()
