"""[Log Helper]

Diese Klasse stellt logger Instanzen für die anderen Module als Hilfsklasse zur Verfügung.
"""

import logging


def create_Logger(fileHandler=False, logger_name="undefined"):
    """[Creates Logger]
    
    Keyword Arguments:
        fileHandler {[boolean]} -- Erstellt einen Filehandler (default: {FALSE})
        logger_name {str} -- Name des Loggers (default: {"undefined"})
    
    Returns:
        logging.getLogger() -- Ein logging Objekt
    """

    #Setting Up Logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    #Optional File Logger
    if (fileHandler):
        fh = logging.FileHandler(logger_name + "_01.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    logger.addHandler(ch)
    return logger