#!/usr/bin/env python
#
#   1.31.2013 by johnb
#   Returns a logging instance that logs to the
#   console and to file.
# -----------------------------------------------------------------------------
import logging

def initialize_log(logFile, scriptName='--', ):
    """
    Creates a logging instance of the name {scriptName}.
    The logging instance is returned by the function to
    be used like this:
    log.info(msg)
    This script allows for different levels to be
    displayed to file and printed to screen.  For
    instance, all error and critical level items can be
    written to file only while everything prints to
    screen.  There are many possibilities for this.
    """
    logger = logging.getLogger(scriptName)
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logFile)
    fh.setLevel(logging.INFO)
    # set StreamHandler() log level for printing to screen.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'.format(datefmt='%m/%d/%Y %H:%M:%S'))
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

if __name__ == '__main__':
    LOG_FILENAME = '/path/to/file.log'
    log = initialize_log(LOG_FILENAME, 'Log Test')
    log.debug('debug message')
    log.info('info message')
    log.warn('warn message')
    log.error('error message')
    log.critical('critical message')
