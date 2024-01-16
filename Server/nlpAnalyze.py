import string

sentences = [
    'i love my dog',
    'I, love my cat',
    'You love my dog!'
]

sentences1 = [
    "This is a sample sentence.", 
    "Another sentence with duplicate words.",
    "This is a sample sentence."
]

def assign_values(sentences):
    word_values = {}
    result = {}

    for sentence in sentences:
        words = sentence.split()
        for word in words:
            # Remove punctuation from the word and convert to lowercase
            word = word.strip(string.punctuation).lower()
            
            if word:
                # Check if the processed word is not empty after removing punctuation
                if word not in word_values:
                    word_values[word] = len(word_values) + 1
                result[word] = word_values[word]

    return result

#Example usage:
word_values_dict = assign_values(sentences)
print(word_values_dict)

#empty_tocken = "<OOV>"