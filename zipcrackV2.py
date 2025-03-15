#!/bin/ !python
#:  Title: zipcrackV2 - Cracking Zip files. Mainly for cracking zip files  
#:                   by scraping passwords from Telegram groups/channels, 
#:                  Discord groups/channel if their API still allows.....
#:                  Also allows program to resume from last value in 
#:                  dictionary
#:  Synopsis:   ./tg_ZipCrack.py
#:  Date:   2025-03-12
#:  Version:    2.0
#:  Author: ostronics {fg_daemon}
#:  Options:    -f - Specify zip file
#:              -d - Specify dictionary lists
#:              -t - Specify number of threads
#:  Author:     ostronics
from threading import Thread

import optparse
import pyzipper as pyzipp
import queue
import sys
import threading
import zipfile as zf

#password_found_event = threading.Event()
# Shared event to signal when the password is found
password_found = False
password_found_lock = threading.Lock() # This lock ensures thread-safe access to the flag

def extractFile(zFile1, password):
    '''
        method extract zip file
    '''
    global password_found
    print('[+] Cracking Password... ')
    try:
        # If the password is already found, exit this thread
        with password_found_lock:
            if password_found:
        # Exit early if password is found
        #if password_found_event.is_set():
                return

        # Try setting the password and extracting
        unlock = zFile1.setpassword(password)
        unlock1 = zFile1.extractall()

        # If password is correct
        if unlock and unlock1 is not None:
            with password_found_lock:
                if not password_found: # Ensure only one thread prints the password
                    password_found = True
                    print('\n\n[+] Found password {}\n\n'.format(str(password)))
            # Set the event to signal all threads to stop
            #password_found_event.set()
            #sys.exit(0) # Exit program
    

    except Exception as e:
        pass
        #print('{}'.format(e))

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
    zFile1 = pyzipp.AESZipFile(zname) # using the pyzipper module
    passFile = open(dname) # Opening dictionary wordlists file
    

    # Iterate over password list
    for lines in passFile.read().split():
        #for lines in passFile.split():
        password = lines.strip('\n')
        password = bytes(password.encode())

        # If the password is found, break out of the loop and stop further threads
        with password_found_lock:
            if password_found:
            #if password_found_event.is_set():
                print("\n[+] Password found, stopping brute force...\n")
                break

        # Start multiple threads to test passwords concurrently
        for _ in range(THREADS):
            t = threading.Thread(target=extractFile, args=(zFile1, password))
            t.daemon = True # Make thread a daemon so it can exit immediately whe the main program ends
            t.start()
            #t.join() # Wait for thread to finish before starting the next one

        # Wait briefly to give threads time to attempt extraction,
        # without making the program wait for each thread to finish.
        threading.Event().wait(0.05) # Adjust  sleep time if needed to balance performance

if __name__ == '__main__':
    parser = optparse.OptionParser("python zipcrack.py "+\
            "-f <zipfile> -d <dictionary> -t <1>")
    parser.add_option('-f', dest='zname', type='string',\
            help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
            help='specify dictionary file')
    parser.add_option('-t', dest='tthread', type='int',\
            help='specify the number of threads')

    (options, args) = parser.parse_args()

    if (options.zname == None) | (options.dname == None) | (options.tthread == None):
        print(parser.usage)
        exit(0)
    else:
        THREADS = options.tthread
        zname = options.zname
        dname = options.dname

    main()
