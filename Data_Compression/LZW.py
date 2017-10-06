#!/usr/bin/python
# coding: utf-8

import os
import sys
import collections
import time
import glob
from lab01_entropy import process_string

L = 100000 # maximum length
# dict_init = collections.defaultdict(str)

def mysort(comb_):
    str = []
    size = len(comb_)
    for c in comb_:
        str.append(c)
    str.sort()
    return ''.join(str)

class lzw_encoder:

    def __init__(self, text):
        self.next_code = 0
        self.dictionary = dict()
        self.dict_init = dict()
        for i in range(0, len(text)):
            # if not self.dictionary.has_key(chr(ord(text[i]))): ###
            self.add_to_dictionary(chr(ord(text[i])))
        self.dict_init = self.dictionary
        self.init_code = self.next_code
    def add_to_dictionary(self, str):
        self.dictionary[str] = self.next_code
        self.next_code += 1
    def encode(self, text):
        ret = [] # inicializa a lista (arquivo de saída)
        P = '' # inicializa o acumulador de caracteres lidos
        for i in range(0, len(text)):
            c = text[i]
            if len(P) == 0 or self.dictionary.has_key(P + c):
                P = P + c
            else:
                code = self.dictionary[P] # quando encontramos a maior cadeia presente emitimos o código dessa cadeia
                self.add_to_dictionary(P + c) # e criamos uma nova cadeia, acrescentando o último caractere lido.
                P = c
                ret = ret + [code]
            if i>0 and i%L == 0:
                self.dictionary = self.dict_init;
        if P:
            ret = ret + [self.dictionary[P]]
        bin_ret = ""
        for x in ret:
            bin_ret += str(bin(x))[2:]
        return ret, bin_ret

class lzw_decoder:
    def __init__(self, text):
        self.next_code = 0
        self.dictionary = dict()
        for i in range(0, len(text)):
            if not self.dictionary.has_key(chr(ord(text[i]))):
                self.add_to_dictionary(chr(ord(text[i])))
    def add_to_dictionary(self, str):
        self.dictionary[self.next_code] = str
        self.next_code += 1
    def decode(self, symbols):
        last_symbol = symbols[0]
        ret = self.dictionary[last_symbol]
        for symbol in symbols[1:]:
            if self.dictionary.has_key(symbol):
                current = self.dictionary[symbol]
                previous = self.dictionary[last_symbol]
                to_add = current[0]
                self.add_to_dictionary(previous + to_add)
                ret = ret + current
            else:
                previous = self.dictionary[last_symbol]
                to_add = previous[0]
                self.add_to_dictionary(previous + to_add)
                ret = ret + previous + to_add
            last_symbol = symbol
        return ret

if __name__ == "__main__":
    textfiles = sorted(glob.glob("textfiles/*.txt"))

    file_results = open('results.txt', "w")
    print("Text_Name                          Text_Entropy  Endoded_Entropy  Encoding_Time(ms)  Decoding_Time(ms)   Size(KB)  Encoded_Size(KB)  Compression_Ratio")
    file_results.write("Text_Name                          Text_Entropy  Endoded_Entropy  Encoding_Time(ms)  Decoding_Time(ms)   Size  Encoded_Size  Compression_Ratio\n")
    for textfile in textfiles:
        text = open(textfile, "r").read()
        # text = "I feel like my heart is being touched by Christ"
        encoder = lzw_encoder(text)
        time_encode = time.time()                               # starting time - encoding
        encoded, bin_encoded = encoder.encode(text)
        time_encode = time.time() - time_encode                 # finishing time - encoding

        decoder = lzw_decoder(text)
        time_decode = time.time()                               # starting time - decoding
        decoded = decoder.decode(encoded)
        time_decode = time.time() - time_decode                 # finishing time - decoding

        # Entropies
        H = process_string(text)
        H_encoded = process_string(bin_encoded)
        H_decoded = process_string(decoded)

        spaces = ""
        name = textfile[10:45]
        if len(name) < 36:
            spaces = " " * (36 - len(name))
        text_size = len(text) / 1024.0
        encoded_size = len(bin_encoded) / (1024.0 * 8)
        compression_rate = encoded_size / text_size
        print("%s%s  %.4f %s %.4f %s %.4f %s %.4f %s %.2f %s %.2f %s %.2f" % (textfile[10:45], spaces, H["H_X"], "\t\t",  H_encoded["H_X"], "\t\t", 1000*time_encode, "\t\t\t", 1000*time_decode, "\t\t", text_size,"\t", encoded_size, "\t", compression_rate))
        file_results.write("%s%s   %.4f \t%s %.4f %s %.4f %s %.4f %s %.2f %s %.2f %s %.2f\n" % (textfile[10:45], spaces, H["H_X"], "\t",  H_encoded["H_X"], "\t", 1000*time_encode, "\t", 1000*time_decode, "\t", text_size, "    " , encoded_size, "\t", compression_rate))

    file_results.close()