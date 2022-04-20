import logging

class Logger:
    def __init__(self, name:str) -> None:    
        logging.basicConfig()
        self.logger = logging.getLogger(f'[{name}]')
        self.logger.setLevel(logging.INFO)
