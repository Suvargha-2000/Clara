import pickle , nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from keras.models import load_model
import numpy as np


sno = WordNetLemmatizer()
nltk.download('wordnet')
model = load_model("data/model.h5")
words , labels  , maxlen = pickle.load(open("data/datas.pkl" , "rb"))
print(labels)

sentence = "is there a chance of rain".split(" ")
for i in range(len(sentence)) :
    try :
        sentence[i] = words.index(sno.lemmatize(sentence[i]))
    except :
        sentence[i] = 0

sentence += [0 for i in range(len(sentence), maxlen)]

result = model.predict(np.asarray(np.array([sentence])))

result = list(result[0])
result = result.index(max(result))

print(labels[result])