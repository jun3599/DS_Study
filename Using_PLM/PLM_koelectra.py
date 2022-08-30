from transformers import AutoTokenizer,  AutoModelForSequenceClassification, TextClassificationPipeline
import pandas as pd 
from tqdm import tqdm 
tqdm.pandas()


# load model
tokenizer = AutoTokenizer.from_pretrained("jaehyeong/koelectra-base-v3-generalized-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained("jaehyeong/koelectra-base-v3-generalized-sentiment-analysis")
sentiment_classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model)


# import data 
data = pd.read_excel('D:/Users/wnsgnl/downloads/sentences.xlsx')
data.drop_duplicates(subset=['sentence'])
data = data.iloc[:1000,:]

data['sa'] = data.sentence.progress_apply(lambda x: sentiment_classifier(str(x)[:511]))
data.to_excel('D:/Users/wnsgnl/Desktop/paper_master2/analysis/data/sentiment_koelectra.xlsx')
print(data)

