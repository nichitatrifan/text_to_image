import logging

class Logger:
    def __init__(self) -> None:    
        logging.basicConfig()
        self.logger = logging.getLogger('[SERVER]')
        self.logger.setLevel(logging.INFO)
