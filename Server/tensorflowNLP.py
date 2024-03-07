import sys
version = sys.version_info[0:2]
#check that version is in 3.9-3.11
if version > (3, 11) or version < (3, 9): 
    raise Exception('Requires python 3.11')

#imports
import tensorflow as tf
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#defining
vocab_size = 10000
embedding_dim = 16
max_length = 100
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"
num_epochs = 30


with open ('./data/data.json', 'r', encoding="utf8") as f:
    datastore = json.load(f)
requests = []
labels = []

for item in datastore:
    requests.append(item['request'])
    parameters = [item['is_order'],item['is_refund'],item['is_status'],item['is_date_change'],item['is_dest_change'],item['is_weather'],item['is_allowed']]
    labels.append(parameters)

#now lets split the data into training and testing
training_size = int(len(requests) * 0.8) #80% of the data will be used for training
training_requests = requests[0:training_size]
testing_requests = requests[training_size:]
training_labels = labels[0:training_size]
testing_labels = labels[training_size:]

tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_requests)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_requests)
training_padded = pad_sequences(training_sequences, padding='post')

testing_sequences = tokenizer.texts_to_sequences(testing_requests)
testing_padded = pad_sequences(testing_sequences, padding='post')


# Need this block to get it to work with TensorFlow 2.x
training_padded = np.array(training_padded)
training_labels = np.array(training_labels)
testing_padded = np.array(testing_padded)
testing_labels = np.array(testing_labels)

#now we will create the model using embedding
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

#now we will train the model
history = model.fit(training_padded, training_labels, epochs=num_epochs, validation_data=(testing_padded, testing_labels), verbose=2)


#testing the model
sentence = ["I would like to order a ticket"]
sequences = tokenizer.texts_to_sequences(sentence)
padded = pad_sequences(sequences, padding='post')
print(model.predict(padded))
