import string

sentences = [
    'I love my dog',
    'I love my cat',
    'You love my dog!',
    'Do you think my dog is amazing?'
]

test_data = [
    'i really love my dog',
    'my dog loves my manatee'
]
def assign_indexes(sentences):
    word_values = {}
    #def empty token
    empty_tocken = "<OOV>"
    word_values[empty_tocken] = len(word_values) + 1
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            # Remove punctuation from the word and convert to lowercase
            word = word.strip(string.punctuation).lower()
            if word:
                # Check if the processed word is not empty after removing punctuation
                if word not in word_values:
                    word_values[word] = len(word_values) + 1

    return word_values

#Example usage to assign index to words:
word_indexes = assign_indexes(sentences)
print("\nWord Index = " , word_indexes)

def text_to_sequences(sentences, word_indexes):
    sequences = []
    for sentence in sentences:
        words = sentence.split()
        sequence = [word_indexes.get(word.strip(string.punctuation).lower(), word_indexes['<OOV>']) for word in words]
        sequences.append(sequence)
    return sequences

#Example usage to turnen sentences to sequences:
sequences = text_to_sequences(sentences, word_indexes)
print("\nSequences = " , sequences)

test_seq = text_to_sequences(test_data, word_indexes)
print("\nTest Sequence = ", test_seq)

def pad_sequences(sequences):
    #get the sequence with the max len
    max_length = max(len(sequence) for sequence in sequences)
    # Pad each sequence with zeros
    padded_sequences = [[0] * (max_length - len(sequence)) + sequence for sequence in sequences]
    return padded_sequences

#Example usage to pad sequences:
padded_data = pad_sequences(sequences)
print("\nPadded Data = ", padded_data)






