# -*- coding: utf-8 -*-
"""
Modify pretrained ResNet50 model
"""



from keras.layers import *
from keras import initializers, regularizers, constraints, optimizers
from keras.models import load_model, Model
from keras.applications import resnet50
import keras.backend as K
import numpy as np


def ResNet50_DB1_NinaPro(input_shape,classes, dropout_rate=0.,dense1=0,dense2=0,dense3=0, batch_norm=False):

    #Load pretrained resnet50 model
    res_model = resnet50.ResNet50(weights='imagenet', include_top=False)
    #Keep 80/174 layers of original ResNet50
    res_model = Model(res_model.input, res_model.layers[80].output)
    # Disassemble layers
    layers = [l for l in res_model.layers]

    # Define input
    x_input = Input(input_shape)
    output_res = res_model(x_input)

    #Classifier 
    if batch_norm is True:    
        x = BatchNormalization()(output_res)    
    x = Flatten()(x)
    x = Dense(dense1, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Dense(dense2, activation='relu')(x) 
    x = Dense(dense3, activation='relu')(x)
    x = Dense(classes, activation='softmax')(x)   # Number of classes
    model = Model(x_input, x ,name='Resnet50_DB1_NinaPro')
    #Freeze first 28 layers for fine tuning
    for layer in model.layers[:-52]:
        layer.trainable = False
   
    return model
   


def getNetwork(network):

    model = Resnet50_DB1_NinaPro
    return model
