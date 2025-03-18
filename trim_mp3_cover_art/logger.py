import logging
from datetime import datetime
from pathlib import Path

import colorlog

class Logger:
    '''
    A utility class to configure and manage logging with support for both file and console outputs.
    '''
    LOG_DIR = Path("./logs")
    FILE_LOG_FORMAT = '%(asctime)s %(levelname)-8s %(name)s %(message)s'
    CONSOLE_LOG_FORMAT = r'%(light_black)s%(asctime)s %(levelname_log_color)s%(levelname)-8s %(purple)s%(name)s %(white)s%(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    @staticmethod
    def get_logger(name: str = __name__) -> logging.Logger:
        '''
        Configure and return a logger instance.

        Parameters
        ----------
        name : str, optional
            Name of the logger, by default __name__

        Returns
        -------
        logging.Logger
            Configured logger instance
        '''
        # Ensure the log directory exists
        Logger.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Configure the logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Add file and console handlers
        logfile_path = Logger.LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        logger.addHandler(Logger._get_file_handler(logfile_path))
        logger.addHandler(Logger._get_console_handler())
        logger.propagate = False  # Prevent duplicate logs if used in parent-child logger hierarchy

        return logger

    @staticmethod
    def _get_file_handler(logfile: Path) -> logging.FileHandler:
        '''
        Create and return a file handler for logging.

        Parameters
        ----------
        logfile : Path
            Path to the log file

        Returns
        -------
        logging.FileHandler
            Configured file handler
        '''
        file_handler = logging.FileHandler(logfile, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(Logger.FILE_LOG_FORMAT))
        return file_handler

    @staticmethod
    def _get_console_handler() -> colorlog.StreamHandler:
        '''
        Create and return a console handler with colored output.

        Returns
        -------
        colorlog.StreamHandler
            Configured console handler
        '''
        handler = colorlog.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            colorlog.ColoredFormatter(
                fmt=Logger.CONSOLE_LOG_FORMAT,
                datefmt=Logger.DATE_FORMAT,
                secondary_log_colors={
                    'levelname': {
                        'DEBUG': 'cyan',
                        'INFO': 'light_blue',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red'
                    },
                }
            )
        )
        return handler
