#!/usr/bin/env python3

import argparse

consonant = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z',]
vocals = ['a', 'i', 'u', 'e', 'o']

def swap_letters(letter,direction,letter_type):
    if direction == 'decode':
        step = len(letter_type)-7
    else:
        step = 7
    return letter.replace(letter, (letter_type*3)[letter_type.index(letter)+step])

def dencode(message,direction='encode'):
    chars = list(message.lower())
    encrypted_message = ''
    for char in chars:
        if char in vocals:
            encrypted_message += swap_letters(char,direction,vocals)
        elif char in consonant:
            encrypted_message += swap_letters(char,direction,consonant)
        else:
            encrypted_message += char
    return encrypted_message

def main():
    parser = argparse.ArgumentParser(description='Move x-step Letter')
    parser.add_argument('-d', '--decode', action='store_true', help='Decode message')
    parser.add_argument('-e', '--encode', action='store_true', help='Encode message')
    parser.add_argument('-m', '--message', default='Some text to encode', required=True, type=str, help="Text to encode or decode")
    args = parser.parse_args()
    if args.encode:
        print(dencode(args.message, 'encode'))
    elif args.decode:
        print(dencode(args.message, 'decode'))   
    else:
        print('usage: mxl.py [-h] [-d] [-e] [-m STRING]')
        print('error: unrecognized arguments')
    
if __name__ == '__main__':
    main()
