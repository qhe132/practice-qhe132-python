from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np
import random

import string

characters = string.digits + string.ascii_uppercase

width,height,n_len,n_class = 170,80,4,len(characters)

def gen(batch_size=32):
    X = np.zeros((batch_size,height,width,3),dtype=np.uint8)
    Y = [np.zeros((batch_size,n_class),dtype=np.uint8) for i in range(n_len)]
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


from keras.models import *
model = load_model('cnn.h5')
num = 0
counter = 0
for i in range(0,1000000000):
    X, y = next(gen(1))
    y_pred = model.predict(X)
    if decode(y) == decode(y_pred):
        judge = "R"
        counter+=1
    else:
        judge = "W"
    num+=1

    '''    
    plt.title('real:%s  pred:%s\n%s'%(decode(y), decode(y_pred), judge))
    plt.imshow(X[0], cmap='gray')
    import pylab
    pylab.show()
    '''
print("%s"%(counter/num))
