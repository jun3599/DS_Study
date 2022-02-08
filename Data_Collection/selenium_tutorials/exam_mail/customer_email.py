# mail을 조회해 넘겨주거나 메일을 추가하거나 제외하기 위한 역할 
# 엑셀을 기반으로 한다. 
# 추가할 기능: 경로에 엑셀 파일이 없을 경우 예외처리 ,, 중복 데이터 제어
# 한계1 .대규모 데이터에 대해 조회시 데이터 프레임의 특성상 노출되는 범위의 제한이 있다. 
import pandas as pd 

class customer_info_management():
    def __init__(self,Table_location) -> None:
        self.Table_location = Table_location
        self.Table = pd.read_excel(self.Table_location)
        self.Table = self.Table[['id', 'name', 'Phone', 'email', 'coustomer_rank']].astype('str')

    def view_Table(self):
        print(self.Table)
    
    def load_Table(self):
        return self.Table

    def view_customer(self):
        while True:
            customer_id = input("확인을 원하는 사용자의 id 값을 입력하세요! (조회를 취소하려면 x를 눌러주세요)\n")
            if customer_id == 'x':
                break

            info = self.Table.loc[self.Table['id'] == customer_id]
            if len(info) == 0:
                print("잘못된 id 값입니다. 다시 확인해주세요!\n")
            else: 
                print(info)
    
    def query_info(self,key, values):
        result = pd.DataFrame(columns=self.Table)
        for element in values:
            temp = self.Table.loc[self.Table[key] == element]
            if len(temp) == 0:
                print("[warning!]: {}: {}에 대한 정보가 Table에 존재하지 않습니다!".format(key, element))
                continue
            result = result.append(temp)
        return result

            
    def add_info(self):
        
        activate = 1
        while activate:
            
            id = input("고객의 id 값을 입력해주세요!\n") 
            name = input("고객의 성명을 입력해 주세요! \n")
            Phone = input("고객의 전화번호를 입력해주세요! ['-'로 구분지어 입력해야함]\n")
            email = input("고객의 email을 입력해주세요\n")
            coustomer_rank = input("고객의 등급을 입력해주세요(소문자)\n").upper()

            new_coustomer = {'id':id, 'name': name, 'Phone': Phone, 'email': email, 'coustomer_rank': coustomer_rank}
            temp_table = self.Table.append(new_coustomer, ignore_index=True)
            print(temp_table)

            intention = input('정보 추가를 계속하시겠습니까? (y/n)\n')
            if intention == 'n':
                break
        
        print(temp_table)
        intention_save = input('변경사항을 저장하시겠습니까?(y/n)\n')
        if intention_save == 'y':
            self.Table = temp_table 
            self.Table.to_excel(self.Table_location, index=False)
        elif intention_save == 'n':
            print("정보 갱신을 취소합니다.\n")
            print(self.Table)

        # 변경된 내용 보여주고 -> 의사를 묻고 -> 저장 
        # 추가할 기능: 데이터 정합성 확인 후 갱신 

    def del_duplicates(self):
        print(self.Table.loc[self.Table.duplicated()]) 
        intention_del = input("중복 정보 삭제를 진행하시겠습니까?(y/n)\n")
        if intention_del == 'y':
            temp_table = self.Table.drop_duplicates()
            print(temp_table)
            confirm = input("정말 삭제하시겠습니까? (y/n)\n")
            if confirm == 'y':
                self.Table = temp_table
                self.Table.to_excel(self.Table_location, index=False)
        print("파일 수정을 종료합니다.\n")
        
    def del_info(self):
        while True:
            print(self.Table)
            del_id = input("삭제를 원하는 정보의 id값을 하나씩 입력해주세요 (종료하시려면 x를 입력해주세요)\n")
            # 종료 ,입력 예외 
            if del_id == 'x':
                break;

            del_info = self.Table.loc[self.Table['id'] == del_id]
            if len(del_info) == 0:
                print('잘못된 id값 입니다.')
            else: 
                temp_table = self.Table.drop(del_info.index)
                print(temp_table)
                confirm = input("정말 삭제? (y/n)\n")
                if confirm == 'y':
                    self.Table = temp_table
                    self.Table.to_excel(self.Table_location, index=False)
                
        print(self.Table)
        print("정보 삭제를 종료합니다.")


# 이후 추가하고 싶은 기능 : 그냥 해당 클레스를 불러오면, 업무가 끝날 때 까지 클레스 안에 있는 메소드를 선택해 작업할 수 있도록?! 
#                          클레스 수행시 원하는 작업 선택 -> 작업 -> 다른 작업 더 할래 ? -> ㅇㅇ -> 번호 입력 

# do = customer_info_management('./customer_info.xlsx')
# while True:
#     what_do_u_wanna_do = input("조회:0, 추가:1, 삭제:2, 중복제거:3 종료:x \n")

#     if what_do_u_wanna_do == 'x':
#         print('서비스를 종료합니다.')
#         break

#     elif what_do_u_wanna_do == '0':
#         do.view_Table()
#     elif what_do_u_wanna_do == '1':
#         do.add_info()
#     elif what_do_u_wanna_do == '2':
#         do.del_info()
#     elif what_do_u_wanna_do == '3':
#         do.del_duplicates()
#     else: 
#         print('잘못된 입력입니다. \n')
    



    