import pandas as pd 

import re 
import nltk
from konlpy.tag import Okt
# 한문 - 한글 혼용 어휘를 한글로 변환해주는 라이브러리 
import hanja 

stopwords = ['이', '있', '하', '것', '들', '그', '되', '수', '이', 
                '보', '않', '없', '나', '사람', '주', '아니', '등', '같', 
                '우리', '때', '년', '가', '한', '지', '대하', '오', '말', 
                '일', '그렇', '위하', '때문', '그것', '두', '말하', '알', 
                '그러나', '받', '못하', '일', '그런', '또', '문제', '더', 
                '사회', '많', '그리고', '좋', '크', '따르', '중', '나오', 
                '가지', '씨', '시키', '만들', '지금', '생각하', '그러', 
                '속', '하나', '집', '살', '모르', '적', '월', '데', 
                '자신', '안', '어떤', '내', '내', '경우', '명', '생각', 
                '시간', '그녀', '다시', '이런', '앞', '보이', '번', '나', 
                '다른', '어떻', '여자', '개', '전', '들', '사실', '이렇', 
                '점', '싶', '말', '정도', '좀', '원', '잘', '통하', '소리', 
                '놓','에','과','만','의','하다']

def translate_Chinese_character(sentence):
    '''
    한자 병음표기 문장을 한글 문장으로 변환합니다. 
    한글자 한글자 소중한 피같은 글씨 보존합시다! 
    [args]
    입력으로 문장을 넣어줍니다. 이후, 데이터프레임에 적용시 .apply를 활용하면 편리합니다.
    [return]
    한자를 변환한 결과 문장
    '''
    return hanja.translate(sentence, 'substitution')

def clean_text(sentence):
    '''
    문장을 입력하면, 한글과 공백 이외의 모든 불필요한 문자를 제거합니다. 
    '''
    pattern = r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]"
    result = re.sub(pattern, '', sentence) 
    
    # 처리 결과, 공백이라면 결측 처리해줍니다. 
    if result == '':
        return float("NaN")

    return result 

def remove_korean_stopwords(sentence):
    '''
    한국어 불용어를 제거합니다. 
    불용어 사전의 출처는 https://bab2min.tistory.com/544#google_vignette 입니다. 
    [args]
    대상 문장을 입력합니다. 
    [return]
    불용어가 제거된 문장입니다. 
    '''
    result = [] 
    for w in sentence.split():
        if w not in stopwords:
            result.append(w)
        else:
            pass 
    result = ' '.join(result)
    
    # 처리 결과가 공백이라면 결측처리 해줍니다. 
    if result == '':
        return float("NaN")

    return result 

def tokenize_korean_sentence_nouns(sentence):
    '''
    한국어 문장에 대한 토큰화를 진행합니다. 
    토큰화 도구로는 Konlpy의 Okt를 활용합니다.  
    +) stem = True옵션을 사용하면 일정수준의 리마타이징을 수행합니다. morphs 메소드 사용시. 
    modify) 토픽 모델링에는 명사 단위로 관계를 파악하는것이 적합하다고 판단. -> okt.nouns로 해당 방식 수정  
    토큰화 진행 후, 각각의 문장에서 불용어 또한 한번 더 제거해줍니다. 
    [args]
    sentence 
    [return]
    tokenized sentence 
    '''
    okt = Okt()
    tokenized = okt.nouns(sentence)
    result = [word for word in tokenized if not word in stopwords]

    return result

def preprocessing_korean(sentence):
    sentence = translate_Chinese_character(sentence)
    sentence = clean_text(sentence)
    sentence = remove_korean_stopwords(sentence)
    sentence = tokenize_korean_sentence_nouns(sentence)

    return sentence 

