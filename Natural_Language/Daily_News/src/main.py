from text_analyzer import * 
from text_manager import * 
import pandas as pd 


News = pd.read_excel('C:\\Users\\wnsgn\\Desktop\\pro_git\\data_science_study\\DS_Study\\result.xlsx')
W = Word_Cloud_Analyzer(News, 'title')
# S.draw_network()
# W.draw_word_cloud()
# S = Semantic_Network_Analyzer(News, 'title')
# S.draw_n_nodes_network(30)
W.draw_word_cloud()