from keras.models import *
from keras.layers import *
from keras.optimizers import *

def unet(sz=image_size):
    x = Input(sz)
    inputs = x
    
    #downsampling
    f = 8 #number of filters
    layers = []
    for i in range(6):
        x = Conv2D(f, 3, activation='relu',padding='same')(x)
        x = Conv2D(f, 3, activation='relu',padding='same')(x)
        layers.append(x)
        x = MaxPooling2D()(x)
        f = f*2
    ff2 = 64

    #bottleneck
    j = len(layers)-1
    x = Conv2D(f, 3, activation='relu',padding='same')(x)
    x = Conv2D(f, 3, activation='relu',padding='same')(x)
    x = Conv2DTranspose(ff2, 2, strides=(2,2),padding='same')(x)
    x = Concatenate(axis=3)([x,layers[j]])
    j = j-1
    
    #upsampling
    for i in range(5):
        ff2 = ff2//2
        f = f//2
        x = Conv2D(f, 3, activation='relu',padding='same')(x)
        x = Conv2D(f, 3, activation='relu',padding='same')(x)
        x = Conv2DTranspose(ff2, 2, strides=(2,2),padding='same')(x)
        x = Concatenate(axis=3)([x,layers[j]])
        j = j-1
    #classification 
    x = Conv2D(f, 3, activation='relu',padding='same')(x)
    x = Conv2D(f, 3, activation='relu',padding='same')(x)
    outputs = Conv2D(1, 1, activation = 'sigmoid')(x)
    model = Model(inputs=[inputs], outputs = [outputs])
    model.compile(optimizer = Adam(lr = 1e-4), loss = 'binary_crossentropy', metrics = ['mean_iou'])
    
    return model
    
        
    
    
    
    
    
    
    
    
    