import numpy as np 
import pandas as pd 
import matplotlib.font_manager as fm

from nltk import bigrams, ngrams, ConditionalFreqDist 
import networkx as nx 
import matplotlib.pyplot as plt

from text_manager import * 

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'

class Semantic_Network_Analyzer():
    def __init__(self,df,target_column):
        '''
        데이터 프레임과 대상 열의 이름을 입력해 초기화 합니다. 
        데이터 전처리 부터 모든 과정을 자동으로 진행합니다. 보고 싶은 결과만 호출하세요! 
        '''
        self.df = df 
        self.target_column = target_column
        # 토큰화 까지 완료된 데이터입니다. 
        self.preprocessed = df[target_column].apply(preprocessing_korean)

        self.make_ngrams()
        self.calculate_conditional_frequency()
        self.make_conditional_frequency_matrix()

    def make_ngrams(self, n=2):
        '''
        토큰화된 문장을 입력받아 n그램화 시켜줍니다. 
        이후, 의미연결망 분석에 사용됩니다.
        해당 함수는 xxx 함수에 내장되어 자동으로 동작합니다.  
        [입력]
        tokenized_sentence: 토큰화된 문장 
        n : 묶을 단어의 갯수 (default) = 2 , 최대 3 
        이상 입력시 에러 
        [출력]
        n그램화 된 문장의 리스트 
        '''
        ngram = []
        if n == 2:
            for sentence in self.preprocessed:
                ngram.append(bigrams(sentence))
        elif n==3: 
            for sentence in self.preprocessed:
                ngram.append(ngrams(sentence, n))
        else: 
            raise Exception("해당 모델에서는 bigram 혹은 trigram만을 지원합니다.")
        
        token = [] 
        for i in ngram:
            token +=(x for x in i)

        self.ngram_n = n 
        self.ngramed_list = token
        return token

    def calculate_conditional_frequency(self):
        '''
        ** 주의! 해당 함수는 문서 전체를 입력해야 합니다. ** 
        해당 함수는 문서를 입력받아 동시 출현 빈도를 계산해 객체를 반환합니다. 
        해당 함수는 다른 함수에 내장되어 사용자가 직접 입력할 일이 앖겠지만, 직접 사용시 주의하시길...
        [입력]
        document : 리스트로 변환된 전체 문장의 집합, 즉 전체 문서 
        '''
        if self.ngram_n == 2:
            self.obj_ConditionalFreqDist = ConditionalFreqDist(self.ngramed_list)
        elif self.ngram_n ==3:
            # 조건부 확률을 (조건, 아이템 )의 튜플을 통해 계산하기 때문. 
            # 즉, 앞의 조건 튜플이 존재할 때, 이후 단어가 나올 확률 
            # 따라서 입력을 2차원튜플로 주어야 함 
            # 4개라면 ((w1, w2, w3),w4) --> 이상은 아시쥬? 근데 이러면 동시 등장 확률이 매우 낮아질듯! bigram 권장 
            condition_pairs = (((w0, w1), w2) for w0, w1, w2 in self.ngramed_list)
            self.obj_ConditionalFreqDist = ConditionalFreqDist(condition_pairs)

    def make_conditional_frequency_matrix(self):
        frequency_matrix = [] 
        for i in self.obj_ConditionalFreqDist.keys(): 
            temp = [] 
            for j in self.obj_ConditionalFreqDist.keys():
                temp.append(self.obj_ConditionalFreqDist[i][j])
            frequency_matrix.append(temp)
        
        freq_df = pd.DataFrame(data=frequency_matrix, index=self.obj_ConditionalFreqDist.keys(), columns=self.obj_ConditionalFreqDist.keys())
        # 배경색 변경 
        freq_df.style.background_gradient(cmap="Spectral_r")

        self.freq_df = freq_df 

    def get_node_size(self, node_values):
        '''
        그래프 객체에서 각 노드의 중심성 지수를 기준으로 노드의 크기를 정합니다. 
        해당 함수는 그래프를 그리는 함수에서 호출되어 노드의 크기를 결정합니다. 
        [입력]
        그래프 각 노드의 중심성 점수(dict) 
        '''
        nsize = np.array([v for v in node_values])
        # normalize
        nsize = 1000 * (nsize-min(nsize)/ (max(nsize) - min(nsize)))    
        return nsize 
    
    def draw_network(self):
        # unicode minus를 사용하지 않기 위한 설정 (minus 깨짐현상 방지)

        # # 글꼴 설정 
        # # plt.rcParams['font.family'] = 'Malgun Gothic'
        # path = 'C:/Windows/Fonts/malgun.ttf'

        # font_name = fm.FontProperties(fname=path, size=50).get_name()

        # plt.rc('font', family=font_name)
        # 그래프 객체 생성, 입력은 인접행렬 
        G = nx.from_pandas_adjacency(self.freq_df)
        centrality_values = nx.degree_centrality(G).values()
        layout = nx.random_layout(G)
        
        options = {
        'font_size': 16,
        'node_color':list(centrality_values),
        'node_size':self.get_node_size(centrality_values),
        'alpha':0.7,
        'cmap': plt.cm.Blues,
        'font_family': 'Malgun Gothic'
        }

        plt.figure(figsize=(15,15))
        plt.axis('off')
        plt.title('뉴스 기사 의미망 분석 결과', fontsize=10)
        nx.draw_networkx(G, pos=layout, **options)
        plt.show()


News = pd.read_excel('C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\DS_Study\\result.xlsx')

S = Semantic_Network_Analyzer(News, 'title')
print(S.df)
print(S.freq_df)
S.draw_network()