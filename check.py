import threading 
import time 
import random 

# Buffer and size 
buffer = [] 
buffer_size = 5 

# Semaphores 
empty = threading.Semaphore(buffer_size) 
full = threading.Semaphore(0) 
mutex = threading.Semaphore(1) 

# Producer function 
def producer(producer_id): 
    while True: 
        item = random.randint(1, 100) 
        empty.acquire() # Wait if buffer is full 
        mutex.acquire() # Enter critical section  
        # Produce an item
        buffer.append(item) 
        print(f"Producer {producer_id} produced: {item} | Buffer: {buffer}") 
        mutex.release() # Exit critical section     
        full.release() # Signal that buffer is not empty        
        time.sleep(random.uniform(0.5, 2)) 

# Consumer function 
def consumer(consumer_id): 
    while True: 
        full.acquire() # Wait if buffer is empty    
        mutex.acquire() # Enter critical section
        # Consume an item    
        item = buffer.pop(0) 
        print(f"Consumer {consumer_id} consumed: {item} | Buffer: {buffer}") 
        mutex.release() # Exit critical section 
        empty.release() # Signal that buffer has space
        time.sleep(random.uniform(0.5, 2)) 

# Create producer and consumer threads 
producers = [threading.Thread(target=producer, args=(i,)) for i in range(2)] 
consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(2)] 

# Start threads 
for p in producers: 
    p.start() 

for c in consumers:
    c.start()