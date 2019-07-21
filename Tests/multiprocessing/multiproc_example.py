import time

#Import Threading classes
import threading
import multiprocessing



def worker_function(runs=100):
    i = 1000
    for c in range (0,runs):
        for x in range (1,500000):
            y = i + 2 / x

def worker_function_multi(runs=100, procnumber=0, return_dict="null"):
    i = 1000
    print("[Proc %s]: Started" %procnumber)
    for c in range (0,runs):
        for x in range (1,500000):
            y = i + 2 / x
    print("[Proc %s]: Finished" %procnumber)
    return_dict[procnumber] = procnumber

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

    ## Zeitmessung ##
    start_time2 = time.time()

    count2 = 100
    
    ##pass variables via shared variables when working with multiproc
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(4):
        ###Asynchrone Arbeitsverteilung###
        p = multiprocessing.Process(target=worker_function_multi, args=(25,i, return_dict))
        jobs.append(p)
        p.start()

    print("[Main] All Jobs started, doing something else...")
    time.sleep(0.2)
    print("[Main] Still doing other stuff...")

    for proc in jobs:
        #Synchronisieren#
        proc.join()

    print("[Main] ", return_dict.values())

    ## Zeitmessung Stop ##
    end_time2 = time.time()

    print("Duration: %s"% (end_time2 - start_time2))
    print("Runs: %s"%count2)
    print("'fps': %s"% (count2 / (end_time2 - start_time2)))

    print("="*40)

    print("Geschwindigkeitsboost um Faktor: %s"% ( (end_time - start_time) /((end_time2 - start_time2) /100)))