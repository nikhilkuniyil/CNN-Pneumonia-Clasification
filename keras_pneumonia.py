# -*- coding: utf-8 -*-
"""keras_pneumonia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1suTugMR2YEpiEq8njcjUc3eTHJqcaWJ5
"""

import keras
from keras import layers, models
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16

import matplotlib.pyplot as plt

train_path = '/content/drive/MyDrive/chest_xray/train'
val_path = '/content/drive/MyDrive/chest_xray/val'
test_path = '/content/drive/MyDrive/chest_xray/test'

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
)

test_datagen = ImageDataGenerator(rescale=1./255)


train_imgs = train_datagen.flow_from_directory(
    train_path,
    target_size=(150,150),
    batch_size=64,
    class_mode='categorical'
)

val_imgs = test_datagen.flow_from_directory(
    val_path,
    target_size=(150,150),
    batch_size=64,
    class_mode='categorical'
)

test_imgs = test_datagen.flow_from_directory(
    test_path,
    target_size=(150,150),
    batch_size=64,
    class_mode='categorical'
)

conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(150,150,3))
conv_base.trainable=False

model = models.Sequential()
model.add(conv_base)
model.add(layers.GlobalAveragePooling2D())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(2, activation='softmax'))
model.summary()

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['acc']
)

history = model.fit(
    train_imgs,
    steps_per_epoch=60,
    epochs=5,
    validation_data=val_imgs
)

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training Accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.title('Testing and Validation Accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training Loss')
plt.plot(epochs, val_loss, 'b', label='Validation Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.title('Testing and Validation Loss')
plt.legend()

eval = model.evaluate(test_imgs)

model.save('/content/drive/MyDrive/chest_xray/pneumonia_classification.h5')