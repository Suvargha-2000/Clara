from nltk.stem import WordNetLemmatizer
import json , nltk


def createData(path = 'clara/training_data/training.json') : 
    sno = WordNetLemmatizer()
    nltk.download('wordnet')

    with open(path) as file:
        data = json.load(file)

    words = []
    labels = []
    sentences = []
    sentences_intent = []
    index = 1
    data = data["intents"]

    for intent in data:
        if intent["tag"] not in labels : 
            labels.append(intent["tag"])
        sentences.append(intent["patterns"])
        sentences_intent.append(intent["tag"])
        for sentence in intent["patterns"]:
            for word in sentence.split(" "):
                if word in words:
                    continue
                words.append(sno.lemmatize(word))
                index += 1

    X = []
    Y = []

    for i in range(len(sentences)):
        for sentence in sentences[i]:
            Y.append(i)
            X.append(sentence.split(" "))

    maxLen = -1
    for i in range(len(X)):
        maxLen = max(len(X[i]), maxLen)
        for j in range(len(X[i])):
            X[i][j] = words.index(sno.lemmatize(X[i][j])) + 1

    for i in range(len(X)):
        X[i] += [0 for i in range(len(X[i]), maxLen)]
    
    
    # print(X , Y , labels)


    return words , Y , X , labels


