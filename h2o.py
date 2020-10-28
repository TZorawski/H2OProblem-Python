"""
H2O Problem with Python.

Autor: Thais Zorawski
Date: 16/10/2020
"""

from threading import Semaphore, Thread, Lock

import random
import sys


class ElementH(Thread):
    """ Hydrogen Class Thread"""
    
    def __init__ (self, num, semaphoreH, semaphoreO):
        sys.stdout.write("Making element H " +str(num) + "\n")
        Thread.__init__(self)
        self.num = num # ID of thread
        self.semaphoreH = semaphoreH # Hydrogen semaphore
        self.semaphoreO = semaphoreO # Oxygen semaphore

    def run(self):
        # Release resources to 1 Oxygen
        self.semaphoreH.release()
        # Waits for 1 Oxygen
        self.semaphoreO.acquire()
        # --- Built molecule ---
        sys.stdout.write("Hydrogen " +str(self.num) + " connected in a molecule\n")

class ElementO(Thread):
    """ Oxygen Class Thread"""
    
    def __init__ (self, num, semaphoreH, semaphoreO, o_lock):
        sys.stdout.write("Making element O " +str(num) + "\n")
        Thread.__init__(self)
        self.num = num # ID of thread
        self.semaphoreH = semaphoreH # Hydrogen semaphore
        self.semaphoreO = semaphoreO # Oxygen semaphore
        self.o_lock = o_lock # Oxygen lock

    def run(self):
        with self.o_lock: # Only 1 atom can enter here at a time
            # Waits for 2 Hydrogens
            self.semaphoreH.acquire()
            self.semaphoreH.acquire()
            # Release resources to 2 Hydrogens
            self.semaphoreO.release()
            self.semaphoreO.release()
        # --- Built molecule ---
        sys.stdout.write("Oxygen " +str(self.num) + " connected in a molecule\n")

def main():
    """ Programa principal """

    threads = [] # Vector of threads
    num_threads = 20 # Number of threads

    semaphoreH = Semaphore(0) # Control Hydrogens
    semaphoreO = Semaphore(0) # Control Oxygens

    o_lock = Lock() # Oxygen lock

    # Creates and starts the threads
    for thread_number in range(num_threads):

        # Creates the atoms randomly
        element_class = random.randint(0,1)
        if (element_class == 0):
            # Creates Hydrogen
            threads.insert(thread_number, ElementH(thread_number, semaphoreH, semaphoreO))
        else:
            # Creates Oxygen
            threads.insert(thread_number, ElementO(thread_number, semaphoreH, semaphoreO, o_lock))
        threads[thread_number].start()
        

    # Waits the threads
    for thread_number in range(num_threads):
        threads[thread_number].join()

    print("Finished\n")


if __name__ == "__main__":
    main()
