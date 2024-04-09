from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import sys

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

if len(sys.argv) < 2:
    print("No message was sent to the model")
    sys.exit(1)

def main():
    model_path = './saved_model'  # Path to the directory where you saved your trained model
    tokenizer, model = load_model(model_path)
    sentence = sys.argv[1]

    predicted_label = classify_sentence(tokenizer, model, sentence)
    if predicted_label == 0:
        print('you want to order a ticket')
    elif predicted_label == 1:
        print('you want to refund a ticket')
    elif predicted_label == 2:
        print('you want to check the status of your ticket')
    elif predicted_label == 3:
        print('you want to change the date of your ticket')
    elif predicted_label == 4:
        print('you want to change the destination of your ticket')
    elif predicted_label == 5:
        print('you want to know the weather of your destination')
    else:
        print('you want to know what is allowed in the flight')
    print("Predicted Label:", predicted_label)

main()




# def order_ticket(flight_num, seat):
#     # Call the data base - remove the seat from the available seats - and assing it to the user
#     print("You have ordered a ticket for flight number", flight_num, "and seat", seat)
#     return ticket

# def refund_ticket(flight_num, ticket_num):
#     # make sure the ticket is ordered by the user
#     # Call the data base - remove the ticket from the user - and add it to the available seats
#     # print("You have refunded a ticket for flight number", flight_num, "and seat", seat)


# def change_date(flight_num, ticket_num, new_date):
#     # make sure the ticket is ordered by the user
#     # Call the data base - change the date of the ticket
#     print("You have changed the date of the ticket for flight number", flight_num, "to", new_date)

# def change_dest(flight_num, ticket_num, new_dest):
#     # make sure the ticket is ordered by the user
#     # Call the data base - change the destination of the ticket
#     print("You have changed the destination of the ticket for flight number", flight_num, "to", new_dest)