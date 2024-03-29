import json
import numpy as np
import tensorflow.keras as keras
import tensorflow as tf

from sklearn.model_selection import train_test_split

DATA_PATH = "data.json"
SAVED_MODEL_PATH = "model.h5"
LEARNING_RATE = 0.0001
EPOCHS = 50
BATCH_SIZE = 32
NUM_KEYWORDS = 26

def load_dataset(DATA_PATH):
    with open(DATA_PATH, "r") as fp:
        data = json.load(fp)
        
    #extract input and targets
    X = np.array(data["MFCCs"])
    y = np.array(data["labels"])
    
    return X, y

def get_data_splits(DATA_PATH, test_size=0.1, test_validation=0.1):
    #load dataset
    X, y =load_dataset(DATA_PATH)
    
    #create train/validation/test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size)
    X_train, X_validation, y_train, y_validation =train_test_split(X_train, y_train, test_size=test_validation)
    
    #convert inputs from 2d to 3d arrays
    X_train = X_train[..., np.newaxis]
    X_validation = X_validation[..., np.newaxis]
    X_test = X_test[..., np.newaxis]
    
    return X_train, X_validation, X_test, y_train, y_validation, y_test

def build_model(input_shape, LEARNING_RATE, error="sparse_categorical_crossentropy"):
    
    #build network
    model = keras.Sequential()
    
    #CNN conv layer1
    model.add(keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape =input_shape, kernel_regularizer=keras.regularizers.l2(0.001)))
    
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))
    
    #conv layer 2
    model.add(keras.layers.Conv2D(32, (3, 3), activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)))
    
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))
    
    #conv layer 3
    model.add(keras.layers.Conv2D(32, (2, 2), activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)))
    
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))
    
    #flatten the output and fed it into a dense layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation="relu"))
    model.add(keras.layers.Dropout(0.3))

    
    #Softmax classifier
    model.add(keras.layers.Dense(NUM_KEYWORDS, activation="softmax"))
    
    #compile model
    #optimiser = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)
    optimiser = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(optimizer=optimiser, loss=error, metrics=["accuracy"])
    
    #print model overview
    model.summary()
    
    return model

def main():
    #load train/validation/test datasplits
    X_train, X_validation, X_test, y_train, y_validation, y_test = get_data_splits(DATA_PATH)
    
    #build CNN model
    input_shape = (X_train.shape[1], X_train.shape[2], X_train.shape[3]) # segments, coefficients = 13 1
    model = build_model(input_shape, LEARNING_RATE)
    
    #train
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size = BATCH_SIZE, validation_data = (X_validation, y_validation))
    
    #evaluate
    test_error, test_accuracy = model.evaluate(X_test, y_test)
    print(f"Test error: {test_error}, test accuracy{test_accuracy}")
    
    #save
    model.save(SAVED_MODEL_PATH)
    
    
if __name__ =="__main__":
    main()