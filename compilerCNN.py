from __future__ import print_function
import tensorflow.keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
from pathlib import Path
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
from data_load import load_data

def cnn():
    img_size = 140


    x_data, y_data = load_data(img_size)

    x_data = np.array(x_data)  # 462
    y_data = np.array(y_data)

    x_data = np.reshape(x_data,(x_data.shape + (1,)))
    #y_data = np.reshape(y_data,(y_data.shape + (7,)))
    #y_data = np.expand_dims(y_data,axis=)

    print(x_data.shape)
    print(y_data.shape)

    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, stratify=y_data, random_state=0)

    batch_size = 128
    num_classes = 7
    epochs = 100
    dropout_late = 0.4
    earlystopping = EarlyStopping(monitor="val_loss", patience=10)

    # input image dimensions
    img_rows, img_cols = img_size, img_size

    input_shape = (img_rows, img_cols,1)

    model = Sequential()

    model.add(Conv2D(64, kernel_size=(3, 3), input_shape=input_shape, padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(dropout_late))

    model.add(Conv2D(128, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(128, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(dropout_late))

    model.add(Conv2D(256, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(256, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(dropout_late))

    model.add(Conv2D(512, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(512, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(dropout_late))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation("relu"))
    model.add(Dropout(dropout_late))
    model.add(Dense(num_classes, activation='softmax'))

    model.summary()

    model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
              optimizer=tensorflow.keras.optimizers.Adam(learning_rate=0.001),
              metrics=['accuracy'])

    history = model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks=[earlystopping])

    #model = load_model("compilerCNN.h5")
    #for i in range(len(x_test)):
    loss, acc = model.evaluate(x_test, y_test)
    print("acc :", acc)
    print("loss :", loss)

    '''
    score = model.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    '''

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train acc', 'test acc'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
cnn()