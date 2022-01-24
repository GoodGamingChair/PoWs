"""
This is a sha256 PoW using multiprocessing.
Made during rwctf quals 2022

the hash neded to start with 24 bits of zero
"""

import multiprocessing
import hashlib
import string
import itertools
from pwn import *

SERVER_PORT = 1337          #change this
SERVER_IP = '127.0.0.1'     #change this

chars = string.ascii_letters + string.digits
MODE = 'creds'   #3 modes: creds=ip+port; interactive=gets interactive shell; debug=prints the nc output
starts_with = "000000" #change this if needed

context.log_level = 'ERROR'
conn = remote(SERVER_IP, SERVER_PORT)

contains = conn.recv().decode().split('"')[1] #change this if needed
print(f'\n[+] The string should contain: {contains}')

def generate_combinations(length):
    for item in itertools.product(chars, repeat=length):
        string = ''.join(item)
        hash_string(string)

def hash_string(string):
    hash = hashlib.sha256(contains.encode() + string.encode()).hexdigest()

    if hash.startswith(starts_with):
        PORT_STRING = conn.recv().decode().split(': ')[1].split('\n')[0]+"\n" #change this if needed
        SERVER = SERVER_IP  #change this if needed
        print(hash)
        conn.sendline(string.encode())
        if MODE == "creds":
            print("[+] Server ip+port: " + SERVER + ":" + PORT)
        elif MODE == "interactive":
            conn.interactive()
        elif MODE == "debug":
            print(conn.recv())
        pool.terminate()
        pool.close()


print('[+] Running\n')
pool = multiprocessing.Pool()
for i in range(1,6):
    pool.apply_async(generate_combinations, args=(i,))

pool.close()
pool.join()

