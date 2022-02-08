import re 

def read(text_file_location='./mail_contents.txt'):
    contents = ''
    with open(text_file_location, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        title = re.sub("\n", "", lines[0])
        for line in lines[1:]:
            contents += line
    return title, contents

def write(text_file_location='./mail_contents.txt'):
    with open(text_file_location, 'w', encoding='utf-8') as f:
        title = input("제목을 입력하세요.\n")
        f.write(title + "\n")
        i = 1
        while True:
            line = input("문서 {}번째 줄 내용을 입력하세요. (내용의 입력이 끝나면 **를 입력해주세요)".format(i))
            if line == '**':
                break
            f.write(line + "\n")
            i +=1

            
def load_contents(text_file_location ='./mail_contents.txt'):
    text_file_location = text_file_location
    mode = input("이미 작성된 파일의 내용을 입력으로 사용하려면 1번, 지금 작성하려면 2번을 눌러주세요! (1번 권장)\n")
    if mode == '1':
        title, contents = read(text_file_location)
        return title, contents

    elif mode == '2':
        confirm = input("내용을 입력하면, 기존의 파일 내용은 삭제됩니다. 계속 진행하시겠습니까? (y/n)")
        if confirm == 'y':
            write(text_file_location)
            title, contents = read(text_file_location)
            return title, contents
        else: 
            return load_contents()
    else:
        print('잘못된 입력입니다. 다시 입력해주세요\n')
        return load_contents()


