from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import sys
import os
import joblib

# Load tokenizer and model
def load_model(model_path):
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    model = TFBertForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model

# Function to classify a sentence
def classify_sentence(tokenizer, model, sentence):
    # Tokenize and encode the input sentence
    inputs = tokenizer(sentence, return_tensors='tf', padding=True, truncation=True)

    # Make prediction
    logits = model(inputs)[0]

    # Get predicted class label
    predicted_class = tf.argmax(logits, axis=1).numpy()[0]

    return predicted_class

# if len(sys.argv) < 2:
#     print("No message was sent to the model")
#     sys.exit(1)

def analyze_classv0(sentence):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # model_path = os.path.join(current_dir, 'saved_model')  # Path to the directory where you saved your trained model 
    model_path = "server/saved_model"
    tokenizer, model = load_model(model_path)
    predicted_label = classify_sentence(tokenizer, model, sentence)
    
    if predicted_label == 0:
        text = 'you want to order a ticket'
    elif predicted_label == 1:
        text = 'you want to refund a ticket'
    elif predicted_label == 2:
        text = 'you want to check the status of your ticket'
    elif predicted_label == 3:
        text = 'you want to change the date of your ticket'
    elif predicted_label == 4:
        text = 'you want to change the destination of your ticket'
    elif predicted_label == 5:
        text = 'you want to know the weather of your destination'
    else:
        text = 'you want to know what is allowed in the flight'
    print(text)
    print("Predicted Label:", predicted_label)
    return predicted_label, text


def analyze_class(text, confidence_threshold=0.65):
    classifier = joblib.load('server/training/chatbot_model.joblib')
    vectorizer = joblib.load('server/training/vectorizer.joblib')
    text_vectorized = vectorizer.transform([text])
    probabilities = classifier.predict_proba(text_vectorized)[0]
    max_prob = max(probabilities)
    if max_prob >= confidence_threshold:
        pred_class = classifier.classes_[probabilities.argmax()]
        if pred_class == 'order': return 0
        elif pred_class == 'refund': return 1
    else:
        return 2  # This covers both greetings and irrelevant requests