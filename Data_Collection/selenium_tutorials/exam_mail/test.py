# import pandas as pd 
# from customer_email import customer_info_management

# manager = customer_info_management('./customer_info.xlsx')
# table = manager.load_Table()
# print(table)

# test = table[['name', 'email']].to_dict('index')
# print(test)

# f = open('./mail_contents.txt', mode='r', encoding='utf-8')
# a = f.readlines()
# text = ''
# for i in a:
#     text += i
# print(text)
# from selenium import webdriver
# from selenium.webdriver.common import action_chains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

# import time
# import re 

# def read():
#     contents = ''
#     with open('./mail_contents.txt', 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#         title = re.sub("\n", "" ,lines[0])

#         for line in lines[1:]:
#             contents += line
#     return title, contents

# title, contents = read()
# print(title)
# print(contents)

import pandas as pd 
from customer_email import * 

# def test():
#     a =customer_info_management('C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\Web_Scraper_and_Use_API\\selenium_tutorials\\exam_mail\\customer_info.xlsx') 

#     table = a.load_Table()
#     target_user_list = list(map(str, input("발송하고자 하는 고객의 id를 입력해주세요\n").split(' ')))

#     result = pd.DataFrame(columns=table.columns)
#     for id  in target_user_list:
#         temp = table.loc[table['id'] == id]
#         if len(temp) == 0:
#             print("warning: id:{} 고객에 대한 정보는 존재하지 않습니다!".format(id))
#             continue
#         result = result.append(temp)
#     return result

# result = test()
# print(result)
a = customer_info_management('C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\Web_Scraper_and_Use_API\\selenium_tutorials\\exam_mail\\customer_info.xlsx') 
table = a.load_Table()

list1 = table['id'].to_list()
print(list1)