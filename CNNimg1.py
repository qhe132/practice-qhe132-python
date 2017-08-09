from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np
import random

import string

characters = string.digits + string.ascii_uppercase
print(characters)

width, height, n_len, n_class = 170,80,4,len(characters)
#generator = ImageCaptcha(width=width,height=height)
#random_str = ''.join([random.choice(characters) for j in range(4)])
#img = generator.generate_image(random_str)

#plt.imshow(img)
#plt.title(random_str)
#import pylab
#pylab.show()

from keras.utils.np_utils import to_categorical

def gen(batch_size=16):
    X = np.zeros((batch_size,height,width,3),dtype=np.uint8)
    Y = [np.zeros((batch_size,n_class),dtype = np.uint8) for i in range(n_len)]
    generator = ImageCaptcha(width=width,height=height)
    while True:
        for i in range(batch_size):
            random_str = ''.join([random.choice(characters) for j in range(4)])
            X[i] = generator.generate_image(random_str)
            for j,ch in enumerate(random_str):
                Y[j][i, :] = 0
                Y[j][i, characters.find(ch)] = 1
        yield X,Y

def decode(y):
    y = np.argmax(np.array(y),axis=2)[:,0]
    return ''.join([characters[x] for x in y])

X, y = next(gen(1))
plt.imshow(X[0])
plt.title(decode(y))
from keras.models import *
from keras.layers import *
from keras.optimizers import *

input_tensor = Input(shape = (height, width, 3))
x = input_tensor

for i in range(4):
    x = Conv2D(32 * 2 ** i, (3, 3), activation = 'relu')(x)
    x = Conv2D(32 * 2 ** i, (3, 3), activation = 'relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = BatchNormalization(axis=1)(x)

x = Flatten()(x)
x = Dropout(rate = 0.25)(x)
x = [Dense(n_class, activation='softmax', name='c{}'.format(i))(x) for i in range(4)]


model = Model(inputs = input_tensor, outputs = x)

model.compile(optimizer = 'adadelta', loss='categorical_crossentropy', metrics=['accuracy'])
from keras.callbacks import EarlyStopping
#early_stop = EarlyStopping(monitor='val_loss', patience=2)
model.fit_generator(gen(), steps_per_epoch = 1600, epochs = 5, validation_steps = 40, validation_data = gen())

model.save('cnn.h5')
