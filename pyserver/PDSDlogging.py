import logging
import logging.handlers
import subprocess
import sys
import os

import configuration

#Log rotation config vars:
MAX_SIZE = 1000000      #in bytes
BKP_CNT = 5             #number of backups


class PDSDlogging(object):

    def __init__(self,
                logger_name = 'PDSD_WebServer_Logger',
                log_filename=configuration.DEFAULT_LOG_FILE,
                log_level = logging.DEBUG):

        self.logger = logging.getLogger(str(logger_name))
        self.filename = log_filename
        self.handler = None
    
        #This is a default filename. If directory does not
        #exist we will'
        directory = os.path.dirname(log_filename)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        #This if is because Python is, honestly, stupid!
        if not len(self.logger.handlers):
            self.logger.setLevel(log_level)
            fmt = logging.Formatter(("[%(asctime)s] in file: "
                                    "%(filename)s, module: %(module)s"
                                    " at line %(lineno)s in %(funcName)s()"
                                    " | %(levelname)s | %(message)s"))

            # Add the log message handler to the logger
            # Using python's logrotation
            self.handler = logging.handlers.RotatingFileHandler(log_filename, mode='a',
                                                            maxBytes=MAX_SIZE,
                                                            backupCount=BKP_CNT)
            self.handler.setFormatter(fmt)
            self.logger.addHandler(self.handler)

    def log(self, level, message):
        if(level == "info"):
            self.logger.info(message)
        elif(level == "debug"):
            self.logger.debug(message)
        elif(level == "exception"):
            self.logger.exception(message)
        elif(level == "critical"):
            self.logger.critical(message)
        elif(level == "error"):
            self.logger.error(message)
        elif(level == "warning"):
            self.logger.warning(message)
