import numpy as np
from glob import glob
from collections import defaultdict

def get_char_frequency(text):
    """Returns a dictionary that maps each character in a text to its percentual frequency."""

    total_count = len(text)
    frequency = defaultdict(float) # defaultdicts guarantees that unassigned keys have value 0
    for c in text:
        frequency[c] += 1
    for c in frequency:
        frequency[c] /= total_count
    # divinding a single time after summing integers increases accuracy and speed,
    # since you are not adding floats

    return frequency # { char: frequency }

def get_unique_chars(text):
    """Returns a sorted list of the unique characters in a text."""

    char_set = {c for c in text}              # selects unique chars
    char_list = sorted([c for c in char_set]) # puts them into an ordered list
    return char_list
    # it is important to have chars in a list (and not in a set) because the order of characters matters.
    # we will be indexing an array based on the position of each character.

def get_transition_probability_matrix(text):
    """Returns a square matrix in which each cell in the i-th row and j-th column corresponds to the
    probability that the character with index i will be followed by the characther with index j."""

    chars = get_unique_chars(text)
    char_index = {} # maps each character to its index for fast access
    for i, c in enumerate(chars):
        char_index[c] = i

    # creates a square matrix with side corresponding to the number of unique characters
    char_count = len(chars)
    matrix = [[0 for i in range(char_count)] for i in range(char_count)]

    for i in range(1, len(text)): # counts each character transition in the text
        from_index = char_index[text[i-1]]
        to_index = char_index[text[i]]
        matrix[from_index][to_index] += 1
    
    for i in range(char_count): # calculates the probability of each transition
        sum_row = sum(matrix[i])
        for j in range(char_count):
            if sum_row != 0:
                matrix[i][j] /= sum_row

    return matrix # float[from][to]

def process_string(text):
    """Processes a string, calculating its H(X), H(X,Y), H(X|Y), I(X,Y) and unique symbols count."""

    frequency = get_char_frequency(text)
    transition_matrix = get_transition_probability_matrix(text)
    chars = get_unique_chars(text)
    char_count = len(chars)

    frequency_list = [frequency[x] for x in frequency] # puts frequencies from a dict to a list
    H_X = 0 # H(X)
    for f in frequency_list:
        if(f>0):
            H_X += - f * np.log2(f)

    H_XbarY = 0 # H(X|Y)
    for i in range(char_count): # X
        for j in range(char_count): # Y
            P_XbarY = transition_matrix[j][i]
            if (P_XbarY != 0):
                H_XbarY += -frequency[chars[j]] * P_XbarY * np.log2(P_XbarY)
            # else: 0 * np.log2(0) = 0 (definition)

    H_XY = 0 # H(X,Y)
    for i in range(char_count): # X
        for j in range(char_count): # Y
            P_XY = frequency[chars[j]] * transition_matrix[j][i]
            if P_XY != 0:
                H_XY += - P_XY * np.log2(P_XY)
            # else: 0 * np.log2(0) = 0 (definition)

    I_XY = H_X - H_XbarY # I(X,Y)

    return { "H_X": H_X, "H_XbarY": H_XbarY, "H_XY": H_XY, "I_XY": I_XY, "symbol_count": char_count }
