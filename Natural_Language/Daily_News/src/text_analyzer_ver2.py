# from imp import reload
import numpy as np 
import pandas as pd 

from nltk import bigrams, ngrams, ConditionalFreqDist 

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation

from text_manager import * 
from collections import Counter

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx 
from wordcloud import WordCloud 

# 로컬상에 위치한 글꼴의 위치를 지정합니다. 
fontpath= 'C:/Users/wnsgn/AppData/Local/Microsoft/Windows/Fonts/SCDream6.otf'
# font manager에 경로를 넘겨주어 객체를 생성합니다. 
fontprop = fm.FontProperties(fname= fontpath, size=10)
# fontfamily 설정을 변경해줍니다. 
plt.rc('font', family='S-Core Dream')
mpl.font_manager._rebuild()


class text_Analyzer():
    def __init__(self,df,target_column):
        '''
        데이터 프레임과 대상 열의 이름을 입력해 초기화 합니다. 
        데이터 전처리 부터 모든 과정을 자동으로 진행합니다. 보고 싶은 결과만 호출하세요! 
        '''
        self.df = df 
        self.target_column = target_column
        # 토큰화 까지 완료된 데이터입니다. 
        self.preprocessed = df[target_column].apply(preprocessing_korean)

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
        
        # 선행되어야 하는 함수들이 모두 호출되어, 필요한 변수가 생성되었는지 확인합니다. 
        if 'ngramed_list' not in dir(self):
            self.make_ngrams()
            print("n-gram화 완료!(확인을 원하시면 self.ngramed_list로 조회가 가능합니다.)\n")
        if 'obj_ConditionalFreqDist' not in dir(self):
            self.calculate_conditional_frequency()
            print("동시 등장 빈도 계산완료!(확인을 원하시면 self.obj_ConditionalFreqDist를 통해 조회가 가능합니다.)\n")
        if 'freq_df' not in dir(self):
            self.make_conditional_frequency_matrix()
            print('동시 등장 빈도 인접행렬 구성완료!(확인을 원하시면 self.freq_df로 조회 가능합니다!)\n')   

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
        # 선행되어야 하는 함수들이 모두 호출되어, 필요한 변수가 생성되었는지 확인합니다. 
        if 'ngramed_list' not in dir(self):
            self.make_ngrams()
            print("n-gram화 완료!(확인을 원하시면 self.ngramed_list로 조회가 가능합니다.)\n")
        if 'obj_ConditionalFreqDist' not in dir(self):
            self.calculate_conditional_frequency()
            print("동시 등장 빈도 계산완료!(확인을 원하시면 self.obj_ConditionalFreqDist를 통해 조회가 가능합니다.)\n")
        if 'freq_df' not in dir(self):
            self.make_conditional_frequency_matrix()
            print('동시 등장 빈도 인접행렬 구성완료!(확인을 원하시면 self.freq_df로 조회 가능합니다!)\n')   

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


    def count_word(self):
        
        # 1. 데이터를 단어들의 리스트로 변환합니다. 
        words= [] 
        for sentence in self.preprocessed:
            words.extend(sentence)
        
        # 2. 모든 단어의 빈도를 계산합니다.  
        self.word_counter = Counter(words)
        

    def draw_word_cloud(self,n=30):
        if 'word_counter' not in dir(self):
            print("word counter 객체를 생성합니다.")
            self.count_word()
            print("생성이 완료되었습니다.(조회를 원하시면 self.word_counter를 호출해보세요!)")
        # n = int(input("시각화에 포함시킬 상위 단어 n개(숫자)를 입력해주세요: "))
        
        # n번째 요소까지 슬라이싱 이후 dict로 변환 
        top_words = self.word_counter.most_common(n)
        top_words = dict(top_words)

        # 워드클라우드 객체 생성 
        # 배경색 설정 및 사용하고자 하는 글꼴의 위치를 입력해 초기화 
        wc = WordCloud(font_path='C:\\Users\\wnsgn\\AppData\\Local\\Microsoft\\Windows\\Fonts\\SCDream6.otf',background_color='white')
        # 빈도수 기반 생성(입력으로 값:빈도의 dict입력)
        wc.generate_from_frequencies(top_words)

        figure= plt.figure(figsize=(12,12))
        ax = figure.add_subplot(1,1,1)
        ax.axis('off')
        ax.imshow(wc)
        plt.show()
        
    def show_distribution_of_sentence_length(self):
        '''
        해당 함수는 전처리된 문장 각각의 길이 분포에 대한 시각화 결과를 보여줍니다. 
        해당 함수를 사용해 문장 길이의 분포를 확인하고, 문장의 길이가 지나치게 짧은 결과는 
        추후 분석에서 제거 가능하도록 합니다. 
        '''
        sentences_length = list(map(len, self.preprocessed.to_list()))
        sentences_length.sort(reverse=True)

        y_pos = np.arange(len(self.preprocessed))

        plt.figure(figsize=(12,12))
        plt.barh(y_pos, sentences_length)
        plt.ylabel('문장')
        plt.yticks(ticks=[], labels=[])
        plt.title("문장 길이 분포")
        plt.grid(b=True)
        plt.show() 

    def delete_short_sentences(self,n=2):
        '''
        문장의 길이가 n 이하인 문장을 분석 대상에서 제외합니다.
        대상 문장을 제거할 경우, selected_sentence 인스턴스가 생성됩니다. 
        [args]
        n : 문장의 토큰 갯수가 n개 이하인 문장은 분석 대상에서 제외합니다. 
        [result]
        self.selected_sentence 생성 
        ''' 
        sentences = self.preprocessed.to_list()
        # 문장의 리스트(2중 리스트)를 입력받아 -> enumerate를 활용해 문장의 길이가 n이하인 문장의 인덱스를 모두 담습니다. 
        drop_index= [] 
        for index, sentence in enumerate(sentences):
            if len(sentence) < n:
                drop_index.append(index)
        # 인덱스를 활용해 해당 문장을 삭제합니다. 
        self.selected_sentences = np.delete(sentences, drop_index, axis=0)

    def reverse_tokenization(self, tokenized_sentences_list):
        '''
        skilearn의 TfidfVectorizer을 이용하기 위해 토큰화를 되돌리는 작업을 진행합니다. 
        이용자가 직접 호출 할 일은 없지만, 이후 tf-idf행렬 구성시 호출됩니다. 
        [args] 함수에서 자동 호출됩니다. 
        1. 만약 deleted_short_sentence가 호출되어 self.selected_sentences가 생성되었다면, 인자로 self.selcted_sentence가 입력됩니다. 
        2. 그렇지 않은경우 self.preprocessed.to_list()가 직접 입력됩니다. 
        '''
        detokenized_doc= [] 
        for tokenized_sentence in tokenized_sentences_list:
            detokenized = ' '.join(tokenized_sentence)
            detokenized_doc.append(detokenized)
        return detokenized_doc

    def calculate_tfidf(self):
        '''
        앞서, delete_short_sentence의 수행 여부에 따라 다르게 동작합니다. 
        짧은 문장을 제거하고 self.selected_sentece 인스턴스가 생성된 경우 if 문의 내용을 
        선언되지 않은 경우에는 elif문의 내용을 수행합니다. 
        [args] . 
        '''
        if 'selected_sentences' in dir(self):
            detokenized_sentences = self.reverse_tokenization(self.selected_sentences)
        elif 'selected_sentences' not in dir(self):
            tokenized_sentences = self.preprocessed.to_list()
            detokenized_sentences = self.reverse_tokenization(tokenized_sentences)
        
        # tf-idf 행렬을 생성합니다. 
        # 상위 1,000개의 단어를 보존 
        vectorizer = TfidfVectorizer(max_features= 1000)
        X = vectorizer.fit_transform(detokenized_sentences)
        print("TF-IDF행렬 생성 완료!: shape= ",X.shape, '\n self.tfidf 호출시 객체확인 가능')
        self.tfidf = X 
        self.vectorizer = vectorizer

    
    def get_topics(self, components, feature_names, n=10):
        for idx, topic in enumerate(components):
            print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(5)) for i in topic.argsort()[:-n - 1:-1]])

    def latent_sementic_analysis(self):
        '''
        앞서, calculate_tfidf 의 수행 여부에 따라 다르게 동작합니다. 
        이미 tfidf를 계산한 경우 if 문의 내용을 
        선언되지 않은 경우에는 elif문의 내용을 수행합니다. 
        [args] . 
        '''
        if 'tfidf' in dir(self):
            confirm = input("분석에 포함할 문장의 최소 길이를 재지정 하시겠습니까? (y/n) : ")
            if confirm == 'y':
                self.show_distribution_of_sentence_length()
                n = int(input("최소 문장의 길이 n을 입력해주세요, 만약 축소 과정을 취소하시려면 0번을 눌러주세요!"))
                if n > 0:
                    self.delete_short_sentences(n)
                    self.calculate_tfidf()
                pass
            else:
                pass

        elif 'tfidf' not in dir(self):
            confirm = input("분석에 포함할 문장의 최소 길이를 재지정 하시겠습니까? (y/n) : ")
            if confirm == 'y':
                self.show_distribution_of_sentence_length()
                n = int(input("최소 문장의 길이 n을 입력해주세요, 만약 축소를 원치 않으시면 0번을 눌러주세요!"))
                if n > 0:
                    self.delete_short_sentences(n)
                    self.calculate_tfidf()
                else:
                    self.calculate_tfidf()
            else:
                self.calculate_tfidf()

        n_topics= int(input("그룹화를 진행할 토픽의 수를 입력해주세요: "))
        X = self.tfidf

        svd_model = TruncatedSVD(n_components= n_topics, algorithm='randomized', n_iter=100, random_state=807)
        svd_model.fit_transform(X)
        
        self.svd_model = svd_model 
        self.svd_model_n_topics = n_topics
        
        terms = self.vectorizer.get_feature_names() # 단어 집합. 1,000개의 단어가 저장됨
        self.get_topics(svd_model.components_, terms, 10)

    def latent_Dirichlet_allocation(self, n_topics=10):
        '''
        앞서, calculate_tfidf 의 수행 여부에 따라 다르게 동작합니다. 
        이미 tfidf를 계산한 경우 if 문의 내용을 
        선언되지 않은 경우에는 elif문의 내용을 수행합니다. 
        [args] . LatentDirichletAllocation
        '''
        if 'tfidf' in dir(self):
            confirm = input("분석에 포함할 문장의 최소 길이를 재지정 하시겠습니까? (y/n) : ")
            if confirm == 'y':
                self.show_distribution_of_sentence_length()
                n = int(input("최소 문장의 길이 n을 입력해주세요, 만약 축소 과정을 취소하시려면 0번을 눌러주세요!"))
                if n > 0:
                    self.delete_short_sentences(n)
                    self.calculate_tfidf()
                pass
            else:
                pass

        elif 'tfidf' not in dir(self):
            confirm = input("분석에 포함할 문장의 최소 길이를 재지정 하시겠습니까? (y/n) : ")
            if confirm == 'y':
                self.show_distribution_of_sentence_length()
                n = int(input("최소 문장의 길이 n을 입력해주세요, 만약 축소를 원치 않으시면 0번을 눌러주세요!"))
                if n > 0:
                    self.delete_short_sentences(n)
                    self.calculate_tfidf()
                else:
                    self.calculate_tfidf()
            else:
                self.calculate_tfidf()
        
        n_topics= int(input("그룹화를 진행할 토픽의 수를 입력해주세요: "))

        X = self.tfidf

        lda_model = LatentDirichletAllocation(n_components= n_topics, learning_method='online', max_iter=10, random_state=807)
        lda_model.fit_transform(X)

        self.lda_model = lda_model 
        self.lda_model_n_topics = n_topics
        
        terms = self.vectorizer.get_feature_names() # 단어 집합. 1,000개의 단어가 저장됨
        
        print('*'*20)
        print('--- Model validation scores ---')
        print("Log Likelihood Score: ", lda_model.score(X))
        print("Perplexity: ", lda_model.perplexity(X))
        print('*'*20)
        self.get_topics(lda_model.components_, terms, 10)

    def visualization_lda_results(self):
        '''
        해당 시각화 방식은 코드에디터에서는 사용이 불가하며, 
        주피터 노트북 내에서만 시각화가 가능합니다. 
        '''
        import pyLDAvis 
        import pyLDAvis.sklearn 
        pyLDAvis.enable_notebook()

        if 'lda_model' not in dir(self):
            self.latent_Dirichlet_allocation()

        # reload(pyLDAvis)
        # reload(pyLDAvis.sklearn)

        lda_model = self.lda_model 
        tfidf = self.tfidf
        vectorizer = self.vectorizer 

        vis = pyLDAvis.sklearn.prepare(lda_model, tfidf, vectorizer)
        # vis = sklearn.prepare(self.lda_model, self.tfidf, self.vectorizer)
        return pyLDAvis.display(vis)
        # pyLDAvis.show(vis)
        # pyLDAvis.save_html(vis, '/result.html')

    def make_main_topic_df(self):
        if 'lda_model' not in dir(self):
            self.latent_Dirichlet_allocation()
        
        # Create Document - Topic Matrix
        data = self.tfidf
        lda_model = self.lda_model
        lda_output = lda_model.fit_transform(data)
        
        n_topics =2 
        # column names
        # topicnames = ["Topic" + str(i) for i in range(lda_model.n_topics)]
        topicnames = ["Topic" + str(i) for i in range(self.lda_model_n_topics)]

        # index names
        docnames = ["Doc" + str(i) for i in range(data.shape[0])]

        # Make the pandas dataframe
        df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)

        # Get dominant topic for each document
        dominant_topic = np.argmax(df_document_topic.values, axis=1)
        df_document_topic['dominant_topic'] = dominant_topic

        # Styling
        def color_green(val):
            color = 'green' if val > .1 else 'black'
            return 'color: {col}'.format(col=color)

        def make_bold(val):
            weight = 700 if val > .1 else 400
            return 'font-weight: {weight}'.format(weight=weight)

        # Apply Style
        # df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)
        df_document_topics = df_document_topic.style.applymap(color_green).applymap(make_bold)
        self.document_topics = df_document_topic

        return df_document_topics

    def find_best_lda_model(self):
        test_components = list(map(int, input('테스트하고자 하는 topic수의 목록을 띄어쓰기로 구분지어 입력후 enter를 눌러주세요.').split( )))
        
        # 추후 수정이 필요한 부분입니다. (수정사항: tf-idf 구성 이전 문장 길이 지정 옵션 및 인터렉션 추가)
        if 'tfidf' not in dir(self):
            self.calculate_tfidf()
        X = self.tfidf

        result_dict= {}
        for n_topics in test_components:
            
            lda_model = LatentDirichletAllocation(n_components= n_topics, learning_method='online', max_iter=10, random_state=807)
            lda_model.fit_transform(X)
            
            result_dict[f'n_topics: {n_topics}'] = {"Log Likelihood Score": lda_model.score(X), "Perplexity": lda_model.perplexity(X)}
        print(pd.DataFrame(result_dict))
    
    # def find_best_lda_model(self):
    #     from sklearn.model_selection import GridSearchCV 
        
    #     # 추후 수정이 필요한 부분입니다. (수정사항: tf-idf 구성 이전 문장 길이 지정 옵션 및 인터렉션 추가)
    #     if 'tfidf' not in dir(self):
    #         self.calculate_tfidf()
        
    #     data = self.tfidf

    #     # lda모델 초기화     
    #     lda_model = LatentDirichletAllocation()

    #     grid = GridSearchCV(cv=None, error_score='raise',
    #                         estimator=LatentDirichletAllocation(learning_method='online', max_iter=10, random_state=807),
    #                         param_grid={'n_components': [3, 4, 5, 6, 7]},
    #                         n_jobs=-1,
    #                         scoring=estimator.score(data),
    #                         verbose=1)

        
    #     grid.fit(data)
    #     print(pd.DataFrame(grid.cv_results_))