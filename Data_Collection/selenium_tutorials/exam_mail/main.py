from auto_mail import auto_mail

auto = auto_mail()
# auto.login('junny3599@gmail.com', 'gkwlak1!')
# user_address = {'박준휘':'wnsgnl8229@gmail.com', '박준휘2':'wnsgnl3599@hanyang.ac.kr', '박준휘3':'wnsgnl3599@naver.com'}
# # print(list(user_address.values()))
# # print(user_address['박준휘'])
# auto.send_mail(users_address=user_address)
auto.login('junny3599@gmail.com', 'gkwlak1!')
auto.send_mail(option=0)

# 추가할 사항:
#   1. 이메일 주소 조회 및 추가 제거 기능 
#   2. 테그 유동적 수정 방안
#   3. 메일에 보낼 내용 추가 + 메일마다 사용자의 이름을 불러주어야 한다. 
