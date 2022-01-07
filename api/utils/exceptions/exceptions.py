class EventNotFound(Exception):
    """Handles invalid event type provided to 
        publishers

        Attributes:
            event_type --> the event that's invalid
            message --> additional message to log or print
    
    """
 
    def __init__(self, event_type: str, message: str ="invalid event"):
        self.event_type = event_type
        self.message = message

    def __repr__(self):
        return f"{self.event_type} --> {self.message}"


class UnexpectedError(Exception):
    """Handles unknown errors

        Attributes:
            message --> additional message to log or print
    
    """
 
    def __init__(self, message: str ="unexpected error occured"):

        self.message = message

    def __repr__(self):
        return {self.message}


class NotFoundError(Exception):
    """Handles not found

        Attributes:
            message --> additional message to log or print
    
    """
 
    def __init__(self, message: str ="element not found"):

        self.message = message

    def __repr__(self):
        return {self.message}