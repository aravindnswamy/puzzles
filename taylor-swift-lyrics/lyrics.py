import random
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

# Step 1: Read and preprocess the lyrics
with open("lyrics.txt", "r") as f:
   # Read the contents of the file and replace newlines with spaces
    data = f.read().replace("\n", " ")
# Split the text into individual words
words = data.split()

# Step 2: Calculate word frequencies
# Use Counter to count the occurrences of each word
word_freq = Counter(words)

# Step 3: Get the 20 most frequent words and their frequencies
top_20_words = word_freq.most_common(20)

# Step 4: Create transition probability matrix
# Get a sorted list of unique words from the lyrics
unique_words = sorted(list(set(words)))

#  Create mappings between words and their indices
word_to_index = {word: i for i, word in enumerate(unique_words)} # Word to index mapping
index_to_word = {i: word for word, i in word_to_index.items()} # Index to word mapping

# Initialize a square matrix to store word transition counts
n = len(unique_words) # Number of unique words
T = np.zeros((n, n)) # Transition matrix initialized with zeros

# Calculate transition probabilities by iterating through consecutive word pairs
for i in range(len(words) - 1):
    current_word = words[i] # Current word in the sequence
    next_word = words[i + 1] # Next word in the sequence
    current_index = word_to_index[current_word] # Index of the current word
    next_index = word_to_index[next_word] # Index of the next word
    T[current_index, next_index] += 1 # Increment the transition count

# Normalize the rows of the transition matrix to get probabilities
T_prob = T / T.sum(axis=1, keepdims=True) # Convert counts to probabilities

# Function to plot the word frequencies as a bar chart
def wordFrequencyPlotGraph():
    plt.figure(figsize=(12, 6))
    plt.bar([word for word, _ in top_20_words], [freq for _, freq in top_20_words])
    plt.title("Top 20 Word Frequencies in Taylor Swift's 1989 Album")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right") # Rotate x-axis labels for better readability
    plt.show()

# Function to find most likely next words with randomness
def find_next_word(word, temperature=1.0):
    """
    Predicts the next word based on the current word using the transition matrix.
    NOTE: Temperature controls the randomness: 
    - Lower temperature = deterministic predictions
    - Higher temperature = more randomness
    """
   # Get the index of the given word
    word_index = word_to_index[word]
   # Get the probabilities of transitioning to the next words
    probabilities = T_prob[word_index]

   # Apply temperature to introduce more randomness
   # Lower temperature makes selection more deterministic
   # Higher temperature makes selection more random
    adjusted_probs = np.power(probabilities, 1 / temperature)
    adjusted_probs /= adjusted_probs.sum()

   # Randomly select next word based on adjusted probabilities
    next_index = np.random.choice(len(probabilities), p=adjusted_probs)
    return index_to_word[next_index]

# Find most likely words to follow 'wildest' and 'shake'
print("\nMost likely word after 'wildest':", find_next_word("wildest"))
print("Most likely word after 'shake':", find_next_word("shake"))

# Function to generate non-deterministic song
def generate_sentence(start_word, max_length=10, temperature=1.0):
    """
    Generates a non-deterministic sentence starting with the given word.
    The temperature parameter controls the creativity/randomness.
    """
    random.seed() # Ensure true randomness for different runs
    current_word = start_word # Start with the given word
    sentence = [current_word] # Initialize the sentence with the start word

    for _ in range(max_length - 1):
        next_word = find_next_word(current_word, temperature) # Predict the next word
        if next_word == "Word not found": # Exit if the next word is not valid
            break
        sentence.append(next_word) # Add the predicted word to the sentence
        current_word = next_word # Update the current word for the next iteration

    return " ".join(sentence) # Return the generated sentence as a string


# Generate multiple non-deterministic sentences
print("\nGenerated 5 different sentences starting with 'you':")
for i in range(5):
    generated_sentence = generate_sentence("you", temperature=2) # Use a higher temperature for variety
    print(f"{i+1}. {generated_sentence}")

wordFrequencyPlotGraph()
