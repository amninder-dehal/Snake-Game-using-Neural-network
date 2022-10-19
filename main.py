
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import preprocessing

data = pd.read_csv('snake_data.csv')[5:]
data=  pd.get_dummies(data.drop(['output','sort'], axis=1))
train, test = train_test_split(data, test_size=0.1, shuffle=False)
train, val = train_test_split(train, test_size=0.1, shuffle= False)

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']

def format_output(data):
    y1 = data.pop('left')
    y1 = np.array(y1)
    y2 = data.pop('right')
    y2 = np.array(y2)
    y3 = data.pop('up')
    y3 = np.array(y3)
    y4 = data.pop('down')
    y4 = np.array(y4)    
    return y1, y2 ,y3, y4

train_stats = train.describe()
train_stats.pop('left')
train_stats.pop('right')
train_stats.pop('up')
train_stats.pop('down')
train_stats = train_stats.transpose()

train_Y = format_output(train)
test_Y = format_output(test)
val_Y = format_output(val)

norm_train_X = np.array(norm(train))
norm_test_X = np.array(norm(test))
norm_val_X = np.array(norm(val))

def build_model():
    # Define model layers.
    input_layer = Input(shape=(len(train .columns),))
    inter_layer= Dense(units='64',activation='relu')(input_layer)
    first_dense = Dense(units='128', activation='relu')(inter_layer)
    y1_output = Dense(units='1', name='left')(first_dense)

    second_dense = Dense(units='128', activation='relu')(first_dense)
    y2_output = Dense(units='1', name='right')(second_dense)

    third_dense = Dense(units='128', activation='relu')(first_dense)
    y3_output = Dense(units='1', name='up')(third_dense)

    four_dense = Dense(units='128', activation='relu')(first_dense)
    y4_output = Dense(units='1', name='down')(four_dense)

    # Define the model with the input layer and a list of output layers
    model = Model(inputs=input_layer, outputs=[y1_output, y2_output, y3_output, y4_output])

    return model

model = build_model()

optimizer = tf.keras.optimizers.SGD(lr=0.001)
model.compile(optimizer=optimizer, loss={'left': 'mse', 'right': 'mse','up': 'mse', 'down': 'mse'},
              metrics={'left': tf.keras.metrics.RootMeanSquaredError(),'right': tf.keras.metrics.RootMeanSquaredError(),'down': tf.keras.metrics.RootMeanSquaredError(),
                       'up': tf.keras.metrics.RootMeanSquaredError()})

# model.compile(optimizer=tf.keras.optimizers.RMSprop(1e-3),loss=['binary_crossentropy','binary_crossentropy','binary_crossentropy','binary_crossentropy'],metrics=['acc'])


history = model.fit(norm_train_X, train_Y,  epochs=200, batch_size=1)



















import paho.mqtt.client as mqtt
from sklearn import preprocessing
import json

client = mqtt.Client()
client.connect('broker.mqttdashboard.com')
client.subscribe("topic2")

def predict(value):

    Y_pred = model.predict(preprocessing.normalize(value))
    # print(Y_pred)
    index=Y_pred.index(max(Y_pred))
    print(index)
    client.publish('send',str(index))


def on_message(client, userdata, message):
  msg= str(message.payload.decode('utf-8'))
  
    
  if '[' in msg:
        msg= json.loads(msg)
        lst=[]
        lst.append(msg)
        # print(lst)
        predict(lst)

  else:pass

client.on_message= on_message
client.loop_forever()