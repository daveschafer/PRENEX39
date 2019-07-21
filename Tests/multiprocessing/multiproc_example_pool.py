import time

#Import Threading classes
import threading
import multiprocessing
from multiprocessing import Pool




def worker_function(runs=100):
    i = 1000
    for c in range (0,runs):
        for x in range (1,50000):
            y = i + 2 / x

def worker_function_multi(runs=100, procnumber=0):
    i = 1000
    print("[Proc %s]: Started" %procnumber)
    for c in range (0,runs):
        for x in range (1,50000):
            y = i + 2 / x
    print("[Proc %s]: Finished" %procnumber)
    return procnumber

#wichtig: Multiprocessing muss in einem main modul gestartet werden, ansonsten
#wissen die subprocceses nicht wo ansiedeln
if __name__ == '__main__':
    print("="*40)
    print("Single Core Solution\n")

    ## Zeitmessung ##
    start_time = time.time()
    count = 100
    worker_function(runs=count)

    ## Zeitmessung Stop##
    end_time = time.time()

    print("Duration: %s"% (end_time - start_time))
    print("Runs: %s"%count)
    print("'fps': %s"% (count / (end_time - start_time)))

    time.sleep(1)

    print("="*40)
    print("Multi Core Solution\n")

    pool = Pool(processes=4)

    ## Zeitmessung ##
    start_time2 = time.time()

    count2 = 100
    
    ##pass variables via shared variables when working with multiproc

    jobs = []
    results = list(range(4))
    for i in range(4):
        results[i] = pool.apply_async(worker_function_multi, (25,i,))


    print("[Main] All Jobs started, doing something else...")
    time.sleep(0.2)
    print("[Main] Still doing other stuff...")

    for i in range(4):
        print("[Result]: %s"%results[i].get(timeout=10)) #wait max 1s for result

    print("[Main] ", results)

    ## Zeitmessung Stop ##
    end_time2 = time.time()

    print("Duration: %s"% (end_time2 - start_time2))
    print("Runs: %s"%count2)
    print("'fps': %s"% (count2 / (end_time2 - start_time2)))

    print("="*40)

    print("Geschwindigkeitsboost um Faktor: %s"% ( (end_time - start_time) /((end_time2 - start_time2) /100)))

    print("="*40)
    print("endless loop")
    i =0
    while True:
        pool.apply_async(worker_function_multi, (25,i,))
        i = i+1
