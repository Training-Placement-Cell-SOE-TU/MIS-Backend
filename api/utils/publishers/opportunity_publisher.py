from utils.exceptions.exceptions import *
from utils.publishers.publishers import Publisher


class OpportunityPublisher(Publisher):
    """Notifies subscribers about new internships
        and new job alerts

        Attributes:
            cls.subscribers --> {event1 : [subscriber1, ...], ...} 
                maintains dictionary of subcribers
                for internships and jobs
    """

    subscribers = dict()
    

    @classmethod
    def notify(cls, event_type: str, batches: list[int]):
        """Triggers subscriber functions of a 
            certain event
        """
        
        try:
            for fn in cls.subscribers[event_type]:

                fn(batches)
        
        except KeyError as e:

            #TODO: log to logger

            raise EventNotFound(event_type)

        except Exception as e:

            #TODO: log to logger

            raise UnexpectedError()


    @classmethod
    def attach(cls, event_type: str, fn):
        """Adds subscribers to an event. """
        
        try:
            if event_type not in cls.subscriber:
                cls.subscriber[event_type] = []
        
            cls.subscriber[event_type].append(fn)

        except Exception as e:

            #TODO: log to logger

            raise UnexpectedError()


    @classmethod
    def dettach(cls, event_type: str, fn):
        """Removes subscriber from an event"""

        try:
            if event_type not in cls.subscriber:

                raise KeyError()

            else:

                cls.subscriber[event_type].remove(fn)
            
        except KeyError as e:

            #TODO: log to logger

            raise EventNotFound(event_type)

        except ValueError as e:

            #TODO: log to logger

            raise NotFoundError(f"{fn} --> not a {event_type} cls.subscriber")

        except Exception as e:

            #TODO: log to logger

            raise UnexpectedError()
