from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 

import random
import time

def return_webdriver_location(file_path='C:\\Users\\wnsgn\\Desktop\\chromedriver.exe'):
    return file_path 

def initialize_options():
    
    useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    ,'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    ,'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36']

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent={}".format(useragents[random.randint(0,2)]))
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-gpu" ) # gpu(그래픽 카드 가속) 사용 안하도록 설정
    
    return options 


def fill_header(driver):
    useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    ,'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    ,'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36']

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['en-US', 'en']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": '{}'.format(useragents[random.randint(0,2)])})

    return driver

def check_and_delete_popup(driver):
    windows = driver.window_handles
    if len(windows) > 1:
        for window in windows:
            driver.switch_to_windows(window)
            driver.close() 
        driver.switch_to_window(windows[0])
    
    return driver 


def deal_with_modal_popup(driver):
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
        # actions.click().perform()
        actions.reset_actions  
        time.sleep(random.randint(2,3))
    except: 
        pass 
    
    return driver

def check_popup(driver):
    windows = driver.window_handles
    if len(windows) > 1:
        return True

def del_popups(driver):
    windows = driver.window_handles
    for window in windows:
        driver.switch_to_windows(window)
        driver.close()
    driver.switch_to_window(windows[0])
    return driver 


# scroll down to the end of the page
def scroll_down(driver,scroll_limit=100):
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    while True:
        # 팝업창 체크 및 제어 
        driver = check_and_delete_popup(driver)
        driver = deal_with_modal_popup(driver)
        
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(1)
        count += 1 
        if count == scroll_limit:
            break; 
            
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        driver = check_and_delete_popup(driver)
        driver = deal_with_modal_popup(driver)
    return driver 

def scroll_down_with_comments_activate(driver,actions):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 팝업창 체크 및 제어 
        driver = check_and_delete_popup(driver)
        driver = deal_with_modal_popup(driver)
        
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(1)

        # 모든 댓글창 활성화 
        while True:
            more_comments_btns = driver.find_elements(By.CSS_SELECTOR,'span.j83agx80.fv0vnmcu.hpfvmrgz')
            if len(more_comments_btns) == 0:
                break
            for more_btn in more_comments_btns:
                actions.move_to_element(more_btn).click().pause(1).perform()
                actions.reset_actions()

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height
        driver = check_and_delete_popup(driver)
        driver = deal_with_modal_popup(driver)
    return driver, actions

def scroll_up(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 팝업창 체크 및 제어 
        driver = check_and_delete_popup(driver)

        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")

        # 1초 대기
        time.sleep(1)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver 
