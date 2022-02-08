import requests

# 세션 객체를 생성하고, 해당 객체에서의 프록시 값을 수정해주는 함수 -> 변경된 세션을 return 
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


# Make a request through the Tor connection
# 해당 사이트는 접속한 ip의 주소를 보여줍니다.
# tor을 사용했을때의 ip는 다음과 같습니다. 
# IP visible through Tor
session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)
# Above should print an IP different than your public IP

# 일반적으로 접속했을때의 IP 
# # Following prints your normal public IP
# # print(requests.get("http://httpbin.org/ip").text)



from stem import Signal
from stem.control import Controller

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="gkwlak1")
        controller.signal(Signal.NEWNYM)

renew_connection()
session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)