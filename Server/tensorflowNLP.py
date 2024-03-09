import sys
version = sys.version_info[0:2]
#check that version is in 3.9-3.11
if version > (3, 11) or version < (3, 9): 
    raise Exception('Requires python 3.11')

#imports

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#defining
vocab_size = 10000
embedding_dim = 16
max_length = 10
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"



with open ('./data/data.json', 'r', encoding="utf8") as f:
    datastore = json.load(f)
requests = []
labels = []
full = []



for item in datastore:
    requests.append(item['request'])
    parameters = [item['is_order'],item['is_refund'],item['is_status'],item['is_date_change'],item['is_dest_change'],item['is_weather'],item['is_allowed']]
    full.append(parameters)
    labels.append(parameters.index(1) + 1)



#lets split the data into training and testing
training_requests, testing_requests, training_labels, testing_labels = train_test_split(requests, labels, test_size=0.2, random_state=42)

tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_requests)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_requests)
training_padded = pad_sequences(training_sequences, padding=padding_type, maxlen=max_length, truncating=trunc_type)

testing_sequences = tokenizer.texts_to_sequences(testing_requests)
testing_padded = pad_sequences(testing_sequences, padding=padding_type, maxlen=max_length, truncating=trunc_type)


# Need this block to get it to work with TensorFlow 2.x
# training_padded = np.array(training_padded)
# training_labels = np.array(training_labels)
# testing_padded = np.array(testing_padded)
# testing_labels = np.array(testing_labels)

#model
model = LogisticRegression(max_iter=1000)
model.fit(training_padded, training_labels)
print(model.score(testing_padded, testing_labels))

#test on a new request
sentence = ["אני רוצה להזמין טיסה לבנקוק ביום שישי הקרוב"]
sequences = tokenizer.texts_to_sequences(sentence)
padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
print(model.predict(padded))


