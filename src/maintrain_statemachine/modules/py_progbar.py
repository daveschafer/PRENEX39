
"""[Simple Python Text Progressbar]

Example Usage:

    #Init with 0
    Import py_progbar as pbar
    pbar.printProgressBar(0, 6, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i in range(6):
        time.sleep(1)
        #Increment pBar
        pbar.printProgressBar(i + 1, 6, prefix = 'Progress:', suffix = 'Complete', length = 50)

"""

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()