# 1 - Considerando el programa noblock.py, realizar un programa que lance 10 procesos hijos que intenten encontrar el nonce para un No-Bloque con una dificultad dada. El hijo que lo encuentre primero debe comunicarse con el padre. Realizar todo utilizando multiprocessing

from multiprocessing import Process, Queue, current_process
import random
import sys

"""
Partes de código extraidas de: 
https://github.com/satwikkansal/python_blockchain_app
"""

from hashlib import sha256
import json



class NoBlock:
    def __init__(self, seed, nonce=0):
        self.seed = seed
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest() #Devuelve el hash del bloque



def proof_of_work(block):
    """
    Function that tries different values of nonce to get a hash
    that satisfies our difficulty criteria.
    """
    difficulty = 4

    computed_hash = block.compute_hash()
    while not computed_hash.startswith('0' * difficulty):
        block.nonce += random.randint(1,10000000)
        computed_hash = block.compute_hash()

    my_queue.put((computed_hash,current_process().name))
    
    
 
b = NoBlock(seed='La semilla que quiera', nonce=0)
h = b.compute_hash()

if __name__ == '__main__':
    procs = []
    my_queue = Queue()
    for i in range(10):
        procs.append(Process(target=proof_of_work, args=(b,)))
        procs[i].start()

ph = ','.join(my_queue.get())
sys.stdout.write('Hash y proceso que termino primero: ' + ph)
