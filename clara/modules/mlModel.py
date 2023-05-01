import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import json
import numpy as np
import pandas as pd 
from sklearn.svm import SVC 
from sklearn.ensemble import RandomForestClassifier

sno = nltk.stem.SnowballStemmer('english')
df = pd.DataFrame()

with open("clara/training_data/training.json") as file:
    data = json.load(file)

data = data["intents"]
sentence_arr = []
labels = []

for intent in data:
    for sentence in intent["patterns"]:
        labels.append(intent["tag"])
        sentence_arr.append((" ".join([sno.stem(x.lower()) for x in sentence.split(" ")])))

df = pd.DataFrame({"text":sentence_arr  , "labels" : labels})
le = LabelEncoder()
transformer = TfidfVectorizer()
Y = le.fit_transform(labels)
X_train = transformer.fit_transform(df["text"])

clf2 = LogisticRegression(C=10 , multi_class="multinomial")
clf2.fit(X_train , Y)

sentence = "log off for today"

result = clf2.predict(transformer.transform([sentence]))
print(le.inverse_transform(result))


clf = SVC(kernel='linear')  
clf.fit(X_train , Y)
result = clf.predict(transformer.transform([sentence]))
print(le.inverse_transform(result))



