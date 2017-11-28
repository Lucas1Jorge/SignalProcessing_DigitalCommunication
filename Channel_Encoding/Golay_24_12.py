import numpy as np
from Hamming_4_7 import *

def rotate_left(array):
    aux = array[0]
    to_return = []
    for i in range (len(array) - 1):
        to_return.append(array[i+1])
    to_return.append(aux)
    return to_return

def generate_B_matrix():
    Bc0 = np.array([1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0])
    Bc = [Bc0]
    aux = Bc0
    for i in range(10):
        aux = rotate_left(aux)
        Bc = np.concatenate([Bc, [aux]], axis=0)

    j = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Bc = np.concatenate([Bc, np.array([j])], axis = 0)

    j.append(0)
    B = np.concatenate([Bc, np.matrix([j]).transpose()], axis=1)

    return B


def encode(u, p):
    B = generate_B_matrix()

    # G matrix
    G = np.concatenate([B, np.eye(12, dtype=int)], axis=1)

    # transmitted vector
    v = mod_2(np.dot(u, G))
    to_return = generate_error(v, p)

    return to_return


def weight(array):
    w = 0
    for i in range(len(array)):
        i += array[i]
    return w


def get_syndromes_dictionary():
    syndromes_dictionary = {}
    B = generate_B_matrix()
    Ht = np.concatenate([np.eye(12, dtype=int), B], axis=1).transpose()

    # 1 bit error
    for i in range(24):
        err = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        err[i] = 1
        syndrome = np.dot(err, Ht).tolist()[0]
        syndromes_dictionary[to_string(syndrome)] = err

    # 2 bit error
    for i in range(24):
        for j in range(i - 1):
            err = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            err[i] = 1
            err[j] = 1
            syndrome = np.dot(err, Ht).tolist()[0]
            syndromes_dictionary[to_string(syndrome)] = err

    # 3 bit error
    for i in range(24):
        for j in range(i - 1):
            for k in range(j - 1):
                err = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                err[i] = 1
                err[j] = 1
                err[k] = 1
                syndrome = np.dot(err, Ht).tolist()[0]
                syndromes_dictionary[to_string(syndrome)] = err

    return syndromes_dictionary


syndromes_dictionary = get_syndromes_dictionary()
def decode(w):
    B = generate_B_matrix()
    e = np.eye(12, dtype=int)

    # H matrix
    H = np.concatenate([np.eye(12, dtype=int), B], axis=1)

    # syndrome
    syndrome = mod_2(np.dot(w, H.transpose()))

    # if syndrome != 0, there's error
    if np.array(syndrome).any():
        try:
            error = syndromes_dictionary[to_string(syndrome)]
        except KeyError:
            error = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        w = xor(w, error)

    u = w[12:]
    # if(weight(s) <= 3):
    #     print("step 2")
    #     u = s
    # else:
    #     for i in range(12):
    #         if(weight(mod_2(s + B[i])) <= 2):
    #             u = xor(mod_2(s + B[i]), e[i])
    return u


if __name__ == "__main__":
    # u = [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
    # encoded = encode(u)

    # decoded = decode(encoded)
    # decoded = decode([0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0])
    # print(decoded)

    KxL = 960000
    K = 12
    L = int(KxL / K)
    p = 0.5

    bits = generate_random_bits(KxL)
    L_groups = get_K_groups(bits, K)

    p_values = []
    percentual_differences = []
    while p > 10 ** (-5):
        L_groups_decoded = []
        sum_diff = 0
        for i in range(L):
            encoded = encode(L_groups[i], p)
            L_groups_decoded.append(decode(encoded))
            sum_diff += difference_weight(L_groups[i], L_groups_decoded[i])

        percentual_difference = sum_diff / KxL
        # print("diff: {:.2f}%".format(100.0*percentual_difference))

        p_values.append(p)
        percentual_differences.append(percentual_difference)
        p /= 2

    pyplot.plot(p_values, percentual_differences, color='green')
    pyplot.plot(p_values, p_values, color='blue')
    # pyplot.show()

    main()