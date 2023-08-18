import logging

class BodyAlreadyExistsException(Exception):
    "Raised when the body already exists in body system"
    
    def __init__(self, body):
        self.message = f"The {body.name} already exists in body system"
        logging.error(self.message)
        super().__init__(self.message)