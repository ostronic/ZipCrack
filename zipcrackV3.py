#!/bin/ !python
#: Super Fast
#:  Title: zipcrackV3 - Cracking Zip files. Mainly for cracking zip files  
#:                   by scraping passwords from Telegram groups/channels, 
#:                  Discord groups/channel if their API still allows.....
#:                  Also allows program to resume from last value in 
#:                  dictionary
#:  Synopsis:   zipcrackV3.py
#:  Date:   2025-03-14
#:  Version:    3.0
#:  Author: ostronics {fg_daemon}
#:  Options:    -f - Specify zip file
#:              -d - Specify dictionary lists
#:              -t - Specify number of threads
#:  Author:     ostronics
import threading
import pyzipper
import sys
import optparse
import concurrent.futures

# Shared event to signal when the password is found
password_found = False
password_found_lock = threading.Lock()  # This lock ensures thread-safe access to the flag

def extractFile(zFile1, password):
    '''
        Method to extract zip file
    '''
    global password_found
    print('[+] Cracking Password... ')
    try:
        # If the password is already found, exit this thread
        with password_found_lock:
            if password_found:
                return
        
        # Try setting the password and extracting
        unlock = zFile1.setpassword(password)
        unlock1 = zFile1.extractall()
        
        # If password is correct
        if unlock and unlock1 is not None:
            with password_found_lock:
                if not password_found:  # Ensure only one thread prints the password
                    password_found = True
                    print(f'\n\n[+] Found password {str(password)}\n\n')

    except Exception as e:
        pass  # Optionally, log errors for debugging
        # print(f'{e}')

def main():
    zFile1 = pyzipper.AESZipFile(zname)  # Using the pyzipper module
    passFile = open(dname)  # Opening dictionary file
    
    passwords = [line.strip('\n') for line in passFile.readlines()]
    
    # Using ThreadPoolExecutor for efficient thread management
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        # Submit the password extraction tasks to the thread pool
        futures = []
        for password in passwords:
            # If the password is found, break out of the loop
            with password_found_lock:
                if password_found:
                    print("\n[+] Password found, stopping brute force...\n")
                    break
            future = executor.submit(extractFile, zFile1, bytes(password.encode()))
            futures.append(future)

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

if __name__ == '__main__':
    parser = optparse.OptionParser("python zipcrack.py " + "-f <zipfile> -d <dictionary> -t <1>")
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    parser.add_option('-t', dest='tthread', type='int', help='specify the number of threads')
    
    (options, args) = parser.parse_args()
    
    if (options.zname == None) | (options.dname == None) | (options.tthread == None):
        print(parser.usage)
        exit(0)
    else:
        THREADS = options.tthread
        zname = options.zname
        dname = options.dname
    
    main()

