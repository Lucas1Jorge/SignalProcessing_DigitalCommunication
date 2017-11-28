import numpy as np
import random
from matplotlib import pyplot

def encode(u, p):
    G = np.matrix('1 0 0 0 1 1 1; 0 1 0 0 1 0 1; 0 0 1 0 1 1 0; 0 0 0 1 0 1 1')
    v = mod_2(np.dot(u, G))
    to_return = generate_error(v, p)
    return to_return

def mod_2(array):
    v = []
    for i in range(0, array.size):
        v.append(array.item(i) % 2)
    return v

def xor(list1, list2):
    assert len(list1) == len(list2)
    to_return = []
    for i in range(0, len(list1)):
        to_return.append(list1[i] ^ list2[i])
    return to_return

def generate_random_bits(len):
    bits = []
    for i in range(0, len):
        bits.append(0 if random.random() < 0.5 else 1);
    return bits

def get_K_groups(bits, K):
    groups = []
    for i in range(0, len(bits), K):
        groups.append(bits[i:i+K])
    return groups

def generate_error(v, p):
    error = []
    for i in range(len(v)):
        error.append(0)
        if random.random() < p:
            error[i] = 1
    return xor(v, error)

def difference_weight(array1, array2):
    assert len(array1) == len(array2)
    diff = 0
    for i in range(len(array1)):
        if array1[i] != array2[i]:
            diff += 1
    return diff


def to_string(array):
    str = ""
    for i in range(0, len(array)):
        str += ('0' if array[i]==0 else '1')
    return str

def get_syndromes_dictionary():
    Ht = np.matrix('1 1 1; 1 0 1; 1 1 0; 0 1 1; 1 0 0; 0 1 0; 0 0 1')
    syndromes_dictionary = {}
    for i in range(1, 7):
        err = [0, 0, 0, 0, 0, 0, 0]
        err[i] = 1
        syndrome = np.dot(err, Ht).tolist()[0]
        syndromes_dictionary[to_string(syndrome)] = err
    return syndromes_dictionary

syndromes_dictionary = get_syndromes_dictionary()
def decode(r):
    Ht = np.matrix('1 1 1; 1 0 1; 1 1 0; 0 1 1; 1 0 0; 0 1 0; 0 0 1')
    syndrome = mod_2(np.dot(r, Ht))

    # if syndrome != 0, there's error
    if np.array(syndrome).any():
        try:
            error = syndromes_dictionary[to_string(syndrome)]
        except KeyError:
            error = [0, 0, 0, 0, 0, 0, 0]
        r = xor(r, error)

    R = np.matrix('1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1; 0 0 0 0; 0 0 0 0; 0 0 0 0')
    u = np.dot(r, R).tolist()[0]
    return u


def main():
    # u = [1, 1, 1, 0]
    # encoded = encode(u, 0)
    #
    # decoded = decode(encoded)
    # print(decode([1, 1, 1, 0, 1, 1, 0]))

    KxL = 9600000
    K = 4
    L = int(KxL/K)
    p = 0.5

    bits = generate_random_bits(KxL)
    L_groups = get_K_groups(bits, K)

    p_values = []
    percentual_differences = []
    while p > 10**(-5):
        L_groups_decoded = []
        sum_diff = 0
        for i in range(L):
            encoded = encode(L_groups[i], p)
            L_groups_decoded.append(decode(encoded))
            sum_diff += difference_weight(L_groups[i], L_groups_decoded[i])

        percentual_difference = sum_diff/KxL
        # print("diff: {:.2f}%".format(100.0*percentual_difference))

        p_values.append(p)
        percentual_differences.append(percentual_difference)
        p /= 2

    pyplot.plot(p_values, percentual_differences, color='red')
    # pyplot.yscale('log')
    pyplot.ylabel('Percentual of errors')
    pyplot.xlabel('probability of error')
    pyplot.show()

if __name__ == "__main__":
    main()