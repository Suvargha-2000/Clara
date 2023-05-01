from createTrainingData import createData
import tensorflow as tf
from keras import layers, models
from sklearn.model_selection import train_test_split
import numpy as np
import pickle


def createModel() :

    words , Y , X  , labels = createData()

    pickle.dump((list(words) , labels , len(X[0])) , open("data/datas.pkl" , "wb"))

    Y = tf.keras.utils.to_categorical(Y, num_classes=len(labels))

    X_train, X_test,y_train, y_test = train_test_split(X,Y,
                                    random_state=42, 
                                    test_size=0.1, 
                                    shuffle=True)

    model = models.Sequential()
    model.add(layers.Dense(128, input_shape=(len(X_train[0]),), activation="relu"))
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(32, activation="relu"))
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(32, activation="relu"))
    model.add(layers.Dense(len(labels), activation="sigmoid"))
    model.compile(loss='categorical_crossentropy', 
                optimizer='adam', 
                metrics=['accuracy'])


    model.summary()

    X_train = np.asarray(X_train)
    y_train = np.asarray(y_train)
    X_test = np.asarray(X_test)
    y_test = np.asarray(y_test)


    history = model.fit(X_train , y_train  , epochs=500, batch_size=10 , validation_data=(X_test , y_test))

    model.save("data/model.h5" , history)

createModel()