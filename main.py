import threading
import random
import os

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()
producer_finished = False
consumers_finished = False

# can delete this section if you don't want to reset output files
#----------------------------------------------
#output folder
output_directory = "output_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

#reset output files
def reset_output_files():
    for filename in ["all.txt", "even.txt", "odd.txt"]:
        filepath = os.path.join(output_directory, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
#----------------------------------------------
            
def producer():
    global producer_finished
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            with open(os.path.join(output_directory, "all.txt"), "a") as f:
                f.write(str(num) + "\n")
    producer_finished = True

def consumer_even():
    global consumers_finished
    while not producer_finished or buffer:
        with lock:
            if buffer and buffer[-1] % 2 == 0:
                num = buffer.pop()
                with open(os.path.join(output_directory, "even.txt"), "a") as f:
                    f.write(str(num) + "\n")
            elif not buffer:
                continue
            else:
                continue
    consumers_finished = True

def consumer_odd():
    global consumers_finished
    while not producer_finished or buffer:
        with lock:
            if buffer and buffer[-1] % 2 != 0:
                num = buffer.pop()
                with open(os.path.join(output_directory, "odd.txt"), "a") as f:
                    f.write(str(num) + "\n")
            elif not buffer:
                continue
            else:
                continue
    consumers_finished = True

if __name__ == "__main__":
    # Reset and delete output files if rerun
    reset_output_files()

    producer_thread = threading.Thread(target=producer) 
    consumer_even_thread = threading.Thread(target=consumer_even)
    consumer_odd_thread = threading.Thread(target=consumer_odd)

    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    print("All threads finished.")
