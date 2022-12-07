import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import NLTKWordTokenizer
import pandas as pd
import pickle


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stop_words.update(["'ve", "", "'ll", "'s", ".", ",", "?", "!", "(", ")", "..", "'m", "n", "u"])
    tokenizer = NLTKWordTokenizer()
    
    text = text.lower()
    
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    
    return ' '.join(tokens)

def load_model_db():
    loaded_dict = pickle.load(open("./model/model_db.pickle",'rb'))
    return loaded_dict

def get_prediction(comment,model_name):
    model_dict = load_model_db()
    model = model_dict[str(model_name)]['model']
    count_vectorizer_unique = model_dict[str(model_name)]['count_vectorizer_unique']
    X = preprocess_text(comment)
    s = pd.Series(X)
    X_cv = count_vectorizer_unique.transform(s)
    result = str(model.predict(X_cv)[0])
    result_json = { 'model' : model_name,
            'comment' : comment,
            'rating prediction' : result}
    return result_json


def get_score(model_name):
    model_dict = load_model_db()
    score = model_dict[str(model_name)]['score']
    return { 'model' : model_name,
            'score' : score}