import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import json
import pandas as pd 
from sklearn.svm import SVC 
import pickle , os
from sklearn.model_selection import GridSearchCV

def createModel() :
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

    if not os.path.isfile("data/bestParam.pkl") :
        param_grid = {'C': [0.01, 0.1, 1, 10, 100],
                    'kernel': ['linear', 'poly', 'rbf', 'sigmoid']}

        grid = GridSearchCV(SVC(), param_grid, cv=5)
        grid.fit(X_train, Y)

        print("Best hyperparameters: ", grid.best_params_)
        pickle.dump(grid.best_params_ , open("data/bestParam.pkl" , "wb"))
        grid = grid.best_params_

    else : 
        grid = pickle.load(open("data/bestParam.pkl" , "rb"))

    print(grid)

    clf = SVC(C = grid["C"] , kernel=grid["kernel"])  
    clf.fit(X_train , Y)
    pickle.dump((clf , le , transformer) , open("data/svc.pkl" , "wb"))


def askAi(sentence):
    clf , le , transformer= pickle.load(open("data/svc.pkl" , "rb"))

    result = clf.predict(transformer.transform([sentence]))
    return le.inverse_transform(result)