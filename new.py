# Importing necessary libraries for the chatbot project

# Random module provides functions to generate random numbers and perform random operations.
import random

# JSON module is used for parsing JSON data and working with JSON files.
import json

# Pickle module is used for serializing and deserializing Python objects, which is useful for saving and loading data.
import pickle

# NumPy (numpy) is a powerful library for numerical computations, arrays, and matrices.
import numpy as np

# TensorFlow (tf) is a powerful machine learning library for building and training neural networks.
import tensorflow as tf

# WordNetLemmatizer from NLTK library is used to perform lemmatization on words.
# Lemmatization is the process of reducing words to their base or root form.
from nltk.stem import WordNetLemmatizer

# Import NLTK and download the necessary 'punkt' and 'wordnet' resources

# NLTK (Natural Language Toolkit) is a library for natural language processing (NLP).
# It provides tools and datasets for working with text data.
import nltk

# Download the 'punkt' tokenizer resource from NLTK.
# This resource is required for tokenizing text into sentences and words.
nltk.download('punkt')

# Download the 'wordnet' resource from NLTK.
# This resource is used for lemmatization to find the base form of words.
nltk.download('wordnet')


lemmatizer = WordNetLemmatizer()

# Load intents from the JSON file
intents = json.loads(open(r'C:\Users\hp\Desktop\Python Projects\chatbot\intents.json').read())

words = []
classes = []
documents = []
# List of characters to ignore in user inputs
ignoreLetters = ['?', '!', '.', ',']
# Process each intent in the intents JSON
for intent in intents['intents']:
    # Process each pattern in the intent
    for pattern in intent['patterns']:
        # Tokenize the pattern into a list of words
        wordList = nltk.word_tokenize(pattern)
        # Add the tokenized words to the words list
        words.extend(wordList)
        # Add the tokenized pattern and intent tag to the documents list
        documents.append((wordList, intent['tag']))
        # Add the intent tag to the classes list if not already present
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize the words and remove ignored characters
words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]
# Sort the lists and remove duplicates
words = sorted(set(words))
classes = sorted(set(classes))

# Save the words and classes lists using pickle
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))




"""
outputEmpty = [0] * len(classes):

This syntax creates a list of length len(classes), where each element in the list is initialized to 0.
The multiplication operator (*) repeats the list [0] for the specified number of times (len(classes)).
This creates a list of zeros with the desired length.
"""
training = []
outputEmpty = [0] * len(classes)

# Prepare training data using a bag of words approach
for document in documents:
    bag = []
    wordPatterns = document[0]
    # Lemmatize and convert words to lowercase
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    # Create a bag of words for the pattern
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    # Prepare the output vector for the intent
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    
    # Append the bag of words and output vector to the training data
    training.append(bag + outputRow)

# Shuffle the training data
random.shuffle(training)
# Convert the training data to a NumPy array
training = np.array(training)

# Split the training data into features (trainX) and labels (trainY)
trainX = training[:, :len(words)]
#the points are used for slicing
trainY = training[:, len(words):]

#now we are going to design a neural network model

# Build a sequential neural network
model = tf.keras.Sequential()
# Add a dense layer with 128 units, input shape, and ReLU activation function
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'))
# Add a dropout layer with a 0.5 dropout rate
model.add(tf.keras.layers.Dropout(0.5))
# Add a dense layer with 64 units and ReLU activation function
model.add(tf.keras.layers.Dense(64, activation='relu'))
# Add another dropout layer with a 0.5 dropout rate
model.add(tf.keras.layers.Dropout(0.5))
# Add an output layer with a softmax activation function
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

# Create an SGD optimizer with a learning rate, momentum, and Nesterov momentum
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
# Compile the model using categorical cross-entropy loss, SGD optimizer, and accuracy metric
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)

# Save the trained model to a file
model.save('chatbot_model.h5', hist)
print('Done')


 
