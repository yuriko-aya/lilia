#!/usr/bin/env python3

import argparse

mapping = {'a':'11','b':'12','c':'13','d':'14','e':'15','1':'16',
            'f':'(12)','g':'22','h':'23','i':'24','j':'25','2':'26',
            'k':'(13)','l':'(23)','m':'33','n':'34','o':'35','3':'36',
            'p':'(14)','q':'(24)','r':'(34)','s':'44','t':'45','4':'46',
            'u':'(15)','v':'(25)','w':'(35)','x':'(45)','y':'55','5':'56',
            '6':'(56)','7':'(46)','8':'(36)','9':'(26)','0':'(16)','z':'66',' ':'00'}
             
def dencode(message,direction='encode'):
    if direction == 'decode':
        chars = message.split()
        enc_message = { v:k for k,v in mapping.items()}
        separator = ''
    else:
        chars = list(message.lower())
        enc_message = { k:v for k,v in mapping.items()}
        separator = ' '
    encrypted_message = [enc_message.get(item,item) for item in chars]
    return separator.join(encrypted_message)
    
def main():
    parser = argparse.ArgumentParser(description='Double Number Encoding')
    parser.add_argument('-d', '--decode', action='store_true', help='Decode message')
    parser.add_argument('-e', '--encode', action='store_true', help='Encode message')
    parser.add_argument('-m', '--message', default='Some text to encode', required=True, type=str, help="Text to encode or decode")
    args = parser.parse_args()
    if args.encode:
        print(dencode(args.message, 'encode'))
    elif args.decode:
        print(dencode(args.message, 'decode'))   
    else:
        print('usage: dny.py [-h] [-d] [-e] [-m STRING]')
        print('error: unrecognized arguments')
    
if __name__ == '__main__':
    main()
