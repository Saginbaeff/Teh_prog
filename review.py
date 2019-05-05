import pickle
from collections import Counter
import argparse
import os


def caesar_encode(text, s_key, res_key):
    temp1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
    temp2 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    intab = temp1[s_key % 26:26 + s_key % 26] + temp2[s_key % 26:26 + s_key % 26]
    outtab = temp1[res_key % 26:26+res_key % 26] + temp2[res_key % 26:26+res_key % 26]
    result = text.translate(text.maketrans(intab, outtab))
    return result


def vigenere_encode(text, s_key, r_key):
    counter = 0
    a_up = ord('A')
    a_low = ord('a')
    result = ''
    for i in text:
        if i.isalpha():
            key1 = (ord(s_key[counter % len(s_key)].upper()) - a_up) * i.isupper() + (ord(s_key[counter % len(s_key)].lower()) - a_low) * i.islower()
            key2 = (ord(r_key[counter % len(r_key)].upper()) - a_up) * i.isupper() + (ord(r_key[counter % len(r_key)].lower()) - a_low) * i.islower()
            result += caesar_encode(i, key1, key2)
            counter += 1
        else:
            result += i
    return result


def vernam_encode(text, key):
    symbols = """1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '“”’~`#@!$%^&*()_—-–+={}[]:;",.<>/?\|\n\t"""
    counter = 0
    ans = ''
    for i in text:
        if i in symbols:
            ans += symbols[(symbols.index(i) ^ symbols.index(key[counter])) % 92]
        counter += 1
    return ans


def hack_train(text, file_nm):
    txt = text.upper()
    for i in """ ~`#@!$%^&*()_—-–+={}[]:;",.<>/?\|\n\t1234567890'“”’""":
        txt = txt.replace(i, '')
    symbol_frequency = dict()
    symbol_frequency['MI'] = 0
    for i in Counter(txt).items():
        symbol_frequency[i[0]] = i[1]/len(txt)
        symbol_frequency['MI'] += (i[1]*(i[1] - 1)) / (len(txt)*(len(txt) - 1))
    with open(file_nm, 'wb') as file:
        pickle.dump(symbol_frequency, file)


def hack_sup(slices, text, file_nm):
    with open(file_nm, 'rb') as file:
        model_frequency = pickle.load(file)
    model_frequency.pop('MI')
    res_slices = []
    for i in slices:
        most_suitable = 0
        current_delta = 100000000
        for j in range(0, 26):
            symbol_frequency = {}
            current_slice = caesar_encode(i, j, 0)
            for k in Counter(current_slice).items():
                symbol_frequency[k[0]] = k[1] / len(current_slice)
            slice_delta = 0
            for k in model_frequency.keys():
                try:
                    slice_delta += abs(model_frequency[k] - symbol_frequency[k])
                except KeyError:
                    pass
            if slice_delta < current_delta:
                current_delta = slice_delta
                most_suitable = j
        res_slices.append(list(caesar_encode(i, most_suitable, 0)))
    text_w = ''
    while res_slices:
        i = 0
        while i < len(res_slices):
            text_w += res_slices[i][0]
            res_slices[i].pop(0)
            if not res_slices[i]:
                res_slices.pop(i)
                i -= 1
            i += 1
    txt = list(text)
    j = 0
    for i, k in enumerate(txt):
        if txt[i].isupper():
            txt[i] = text_w[j]
            j += 1
        if txt[i].islower():
            txt[i] = text_w[j].lower()
            j += 1
    result = ''.join(txt)
    return result


def hack(text, file_nm):
    with open(file_nm, 'rb') as file:
        model_frequency = pickle.load(file)
    txt = text.upper()
    for i in """ ~`#@!$%^&*()_—-–+={}[]:;",.<>/?\|\n\t1234567890'“”’""":
        txt = txt.replace(i, '')
    for i in range(1, len(txt) + 1):
        text_slices = []
        for j in range(0, i):
            text_slices.append(txt[j::i])
        for j in text_slices:
            min_index = 0
            for k in Counter(j).items():
                min_index += (k[1] * (k[1] - 1)) / (len(j) * (len(j) - 1))
            if min_index >= model_frequency['MI'] or abs(min_index - model_frequency['MI']) <= 0.01:
                return hack_sup(text_slices, text, file_nm)


PARSER = argparse.ArgumentParser()
SUBPARSERS = PARSER.add_subparsers(dest='command')
ENCODE_PARSER = SUBPARSERS.add_parser('encode')
ENCODE_PARSER.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], required=True)
ENCODE_PARSER.add_argument('--key', required=True)
ENCODE_PARSER.add_argument('--input-file', default='')
ENCODE_PARSER.add_argument('--output-file', default='')
DECODE_PARSER = SUBPARSERS.add_parser('decode')
DECODE_PARSER.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], required=True)
DECODE_PARSER.add_argument('--key', required=True)
DECODE_PARSER.add_argument('--input-file', default='')
DECODE_PARSER.add_argument('--output-file', default='')
TRAIN_PARSER = SUBPARSERS.add_parser('train')
TRAIN_PARSER.add_argument('--text-file', default='')
TRAIN_PARSER.add_argument('--model-file', required=True)
HACK_PARSER = SUBPARSERS.add_parser('hack')
HACK_PARSER.add_argument('--input-file', default='')
HACK_PARSER.add_argument('--output-file', default='')
HACK_PARSER.add_argument('--model-file', required=True)
TEST_PARSER = SUBPARSERS.add_parser('self-test')

ARGS = PARSER.parse_args()

if ARGS.command in ('encode', 'decode'):
    INPUT = ''
    RESULT = ''
    try:
        FILE = open(ARGS.input_file, 'r')
        INPUT = FILE.read()
        FILE.close()
    except OSError:
        INPUT = input()
    if ARGS.cipher == 'caesar':
        if not ARGS.key.isnumeric():
            raise Exception('Caesar key should be a number!')
        if ARGS.command == 'encode':
            RESULT = caesar_encode(INPUT, 0, int(ARGS.key))
        elif ARGS.command == 'decode':
            RESULT = caesar_encode(INPUT, int(ARGS.key), 0)

    elif ARGS.cipher == 'vigenere':
        if not ARGS.key.isalpha():
            raise Exception('Vigenere key should be a word!')
        if ARGS.command == 'encode':
            RESULT = vigenere_encode(INPUT, 'A', ARGS.key)
        elif ARGS.command == 'decode':
            RESULT = vigenere_encode(INPUT, ARGS.key, 'A')

    elif ARGS.cipher == 'vernam':
        if not len(ARGS.key) == len(INPUT):
            raise Exception('Vernam key length should match text length!')
        RESULT = vernam_encode(INPUT, ARGS.key)

    try:
        FILE = open(ARGS.output_file, 'w')
        print(RESULT, file=FILE)
        FILE.close()
    except OSError:
        print(RESULT)

if ARGS.command == 'train':
    INPUT = ''
    try:
        FILE = open(ARGS.text_file, 'r')
        INPUT = FILE.read()
        FILE.close()
    except OSError:
        INPUT = input()
    hack_train(INPUT, ARGS.model_file)

if ARGS.command == 'hack':
    INPUT = ''
    RESULT = ''
    try:
        FILE = open(ARGS.input_file, 'r')
        INPUT = FILE.read()
        FILE.close()
    except OSError:
        INPUT = input()

    RESULT = hack(INPUT, ARGS.model_file)

    try:
        FILE = open(ARGS.output_file, 'w')
        print(RESULT, file=FILE)
        FILE.close()
    except OSError:
        print(RESULT)

if ARGS.command == 'self-test':
    os.system("tests.py")


