#!/bin/ !python
#:  Title: zipcrack - Cracking Zip files. Mainly for cracking zip files  
#:                   by scraping passwords from Telegram groups/channels, 
#:                  Discord groups/channel if their API still allows.....
#:                  Also allows program to resume from last value in 
#:                  dictionary
#:  Synopsis:   ./tg_ZipCrack.py
#:  Date:   2025-03-12
#:  Version:    1.0
#:  Author: ostronics {fg_daemon}
#:  Options:    -f - Specify zip file
#:              -d - 
#:              -t - Specify number of threads
#:  Author:     ostronics
'''unzip with
    with pyzipper.AESZipFile('archive_with_pass.zip') as zf:
    zf.setpassword(b'password')
    zf.extractall('dir_out_pyzipper')
'''
from threading import Thread

import optparse
import pyzipper as pyzipp
import queue
import sys
import threading
import zipfile as zf

def extractFile(zFile1, password):
    '''
        method extract zip file
    '''
    while True:
        try:
            zFile1.setpassword(password)
            zFile1.extractall()
            print('[+] Found password ' + str(password) + '\n\n')
        except Exception as e:
            print(f'{e}')
        #pass
        break

'''
def get_words(resume=None):
     The helper function, which returns the words queue we'll use to 
        bruteforce the zipfile, and contains some special recovery 
        techniques
    
    def extend_words(word):
        
            Because extend_words inner-function will always run in the 
            context of the get_words, so it's place inside the get_words 
            function, to keep the namespace tidy
        
        if word:
         words.put(word)
    # Reading the wordlists from the file
    with open(dname) as file:
        raw_words = file.read()

    found_resume = False
    words = queue.Queue()
    # iteraate over each line
    for word in raw_words.split():
        # Setting the resume variable to the last path of the bruteforcer
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlists from : {resume}')
        else:
            print(word)
            extend_words(word)
    return words
'''

def main():
    parser = optparse.OptionParser("python zipcrack.py "+\
            "-f <zipfile> -d <dictionary> -t <10>")
    parser.add_option('-f', dest='zname', type='string',\
            help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
            help='specify dictionary file')
    parser.add_option('-t', dest='tthread', type='int',\
            help='specify the number of threads')
    (options, args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        THREADS = options.tthread
        zname = options.zname
        #global dname
        dname = options.dname
    #print(zf.is_zipfile(zname))
    zFile1 = pyzipp.AESZipFile(zname) # using the pyzipper module
    #zFile = zf.ZipFile(zname, allowZip64=True)# redacted module lookup pyip
    passFile = open(dname)
    #with open(dname) as file:
        #passFile = file.read()
    for lines in passFile.read().split():
        #for lines in passFile.split():
        password = lines.strip('\n')
        password = bytes(password.encode())
        print(password)
    #word = get_words()
    #print('Press return to continue')
    #sys.stdin.readline()
    #password = word
        print('[+] Cracking Password... ')
        for _ in range(THREADS):
            t = Thread(target=extractFile, args=(zFile1, password))
            t.start()

if __name__ == '__main__':
    main()
