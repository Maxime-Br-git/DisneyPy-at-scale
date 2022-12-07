import pandas as pd
import numpy as np
import pickle
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import NLTKWordTokenizer

#data load and preprocess
df = pd.read_csv('DisneylandReviews.csv', encoding='cp1252',on_bad_lines='skip')
df = df.drop(['Review_ID', 'Year_Month', 'Reviewer_Location'], axis=1)

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stop_words.update(["'ve", "", "'ll", "'s", ".", ",", "?", "!", "(", ")", "..", "'m", "n", "u"])
    tokenizer = NLTKWordTokenizer()
    
    text = text.lower()
    
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    
    return ' '.join(tokens)



df['Review_Text'] = df['Review_Text'].apply(preprocess_text)

#general model
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.model_selection import train_test_split

df1 = df.drop(['Branch'], axis=1)

features = df['Review_Text']
target = df['Rating']


X_train, X_test, y_train, y_test = train_test_split(features, target)

count_vectorizer_unique = CountVectorizer(max_features=2000)

X_train_cv = count_vectorizer_unique.fit_transform(X_train)
X_test_cv = count_vectorizer_unique.transform(X_test)

#creation of a function to retrieve the string of the variable name (usefull for pickle save later on )
import inspect

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

rf_global = RandomForestClassifier(max_depth=3, n_estimators=100)
lr_global = LogisticRegression()
dt_global = DecisionTreeClassifier(max_depth=8)

model_list = [rf_global,lr_global,dt_global]
model_dict = {}

for model_unique in model_list:
  model_dict[retrieve_name(model_unique)[0]]={}
  model_unique.fit(X_train_cv, y_train)
  score = round(model_unique.score(X_test_cv, y_test),2)
  model_dict[retrieve_name(model_unique)[0]]['model'] = model_unique
  model_dict[retrieve_name(model_unique)[0]]['count_vectorizer_unique'] = count_vectorizer_unique
  model_dict[retrieve_name(model_unique)[0]]['score'] = score
  model_dict[retrieve_name(model_unique)[0]]['branch'] = 'all'

# model branch specific

df['Branch'].unique()

for branch in df['Branch'].unique():
    model_name = "rf_{}".format(branch)
    count_vectorizer = CountVectorizer(max_features=2000)
    model = RandomForestClassifier(n_estimators=20, max_depth=5)
    
    df_temp = df[df['Branch'] == branch]
    
    X_train, X_test, y_train, y_test = train_test_split(df_temp['Review_Text'], df_temp['Rating'])
    
    X_train_cv = count_vectorizer.fit_transform(X_train)
    X_test_cv = count_vectorizer.transform(X_test)
    
    model.fit(X_train_cv, y_train)
    score = round(model.score(X_test_cv, y_test),2)


    model_dict[model_name]={}
    model_dict[model_name]['model'] = model
    model_dict[model_name]['count_vectorizer_unique'] = count_vectorizer
    model_dict[model_name]['score'] = score
    model_dict[model_name]['branch'] = str(branch)

print(model_dict)

# save the model to disk
filename = 'model_db.pickle'
pickle.dump(model_dict, open(filename, 'wb'))