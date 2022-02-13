import numpy as np 
import pandas as pd 

from nltk import bigrams, ngrams, ConditionalFreqDist 
import networkx as nx 
import matplotlib.pyplot as plt

from text_manager import * 
from collections import Counter

from wordcloud import WordCloud 

# 폰트 설정 부분 
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.family'] = 'Malgun Gothic'
import matplotlib as mpl
import matplotlib.font_manager as fm

# 로컬상에 위치한 글꼴의 위치를 지정합니다. 
fontpath= 'C:/Users/wnsgn/AppData/Local/Microsoft/Windows/Fonts/SCDream6.otf'
# font manager에 경로를 넘겨주어 객체를 생성합니다. 
fontprop = fm.FontProperties(fname= fontpath, size=10)
# fontfamily 설정을 변경해줍니다. 
plt.rc('font', family='S-Core Dream')
mpl.font_manager._rebuild()


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
        nsize = 1000 * (nsize-min(nsize)) / (max(nsize) - min(nsize))    
        return nsize 
    
    def draw_network(self):

        G = nx.from_pandas_adjacency(self.freq_df)
        centrality_values = nx.degree_centrality(G).values()
        layout = nx.random_layout(G)
        labels = nx.get_edge_attributes(G,'weight')


        options = {
        'font_size': 20,
        'node_color':list(centrality_values),
        'node_size':self.get_node_size(centrality_values),
        'alpha':0.7,
        'cmap': plt.cm.rainbow,
        'font_family': 'S-Core Dream'
        }

        plt.figure(figsize=(20,20))
        plt.axis('off')
        plt.title('뉴스 기사 의미망 분석 결과', fontsize=20)
        nx.draw_networkx(G, pos=layout, **options)
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels = labels);

        plt.show()
    
    def draw_n_nodes_network(self, Top_n=10):
        
        # 가장 높은 등장 횟수를 지니는 상위 n개의 n그램 결과를 가져옵니다. 
        counter = Counter(self.ngramed_list)
        most_n = counter.most_common(Top_n) # 결과: ((word1, word2), 동시 등장 횟수)

        # 노드의 입력을 위해 중복 단어를 제거한 리스트를 생성합니다. 
        most_words = []
        for dummy in most_n:
            most_words.extend(dummy[0]) 
        # 집합 변환 후, 리스트화를 통해 중복제거를 해줍니다.
        most_words = list(set(most_words)) 

        # 그래프 객체를 생성합니다. 
        G = nx.Graph()
        G.add_nodes_from(most_words) # 동시 등장 빈도가 높은 단어들로 노드를 생성합니다. 
        # 간선을 추가합니다. 
        for word_tuple, counter in dict(most_n).items():
            if word_tuple in G.edges():
                weight = G[word_tuple[0]][word_tuple[1]]['weight']
                weight = weight + counter 
                G[word_tuple[0]][word_tuple[1]]['weight'] = weight
            else:
                G.add_edge(word_tuple[0], word_tuple[1], weight= counter)
        
        # 그래프를 출력합니다. 
        centrality_values = nx.degree_centrality(G).values() # 중심성향 값
        layout = nx.random_layout(G) # 레이아웃 지정 옵션 
        labels = nx.get_edge_attributes(G,'weight') # 간선의 가중치 
        options = {'font_size': 16,
                'node_color':list(centrality_values),
                'node_size':self.get_node_size(centrality_values),
                'alpha':0.7,
                'cmap': plt.cm.rainbow,
                'font_family': 'S-Core Dream'}

        plt.figure(figsize=(20,20))
        plt.axis('off')
        plt.title('뉴스 기사 의미망 분석 결과', fontsize=20)
        nx.draw_networkx(G, pos=layout,**options)
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels = labels);
        plt.show()


# # wordcloud 출력을 위한 클레스를 선언합니다. 
# # 추후 모든 분석 관련 class를 하나로 통합할 예정입니다. 
class Word_Cloud_Analyzer():
    def __init__(self,df, target_column):
        self.df = df 
        self.target_column = target_column 

        self.preprocessed = self.df[self.target_column].apply(preprocessing_korean)
        self.count_word()

    def count_word(self):
        
        # 1. 데이터를 단어들의 리스트로 변환합니다. 
        words= [] 
        for sentence in self.preprocessed:
            words.extend(sentence)
        
        # 2. 모든 단어의 빈도를 계산합니다.  
        self.word_counter = Counter(words)
        

    def draw_word_cloud(self,n=30):
        
        # n = int(input("시각화에 포함시킬 상위 단어 n개(숫자)를 입력해주세요: "))
        
        # n번째 요소까지 슬라이싱 이후 dict로 변환 
        top_words = dict(self.word_counter.most_common(n))

        # 워드클라우드 객체 생성 
        # 배경색 설정 및 사용하고자 하는 글꼴의 위치를 입력해 초기화 
        wc = WordCloud(font_path='C:/Users/wnsgn/AppData/Local/Microsoft/Windows/Fonts/GodoB.ttf',background_color='white')
        # 빈도수 기반 생성(입력으로 값:빈도의 dict입력)
        wc.generate_from_frequencies(top_words)

        figure= plt.figure(figsize=(12,12))
        ax = figure.add_subplot(1,1,1)
        ax.axis('off')
        ax.imshow(wc)
        plt.show()

        # 해당 결과는 주피터 노트북 내에서만 확인이 가능합니다. 
        # 이유는 다시 알아 보겠습니다. 

