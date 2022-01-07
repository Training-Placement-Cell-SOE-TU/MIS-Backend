from abc import ABC, abstractmethod

class Publisher:
    """Abstract publisher class 
        notifies subscribers on event triggers
    """

    @abstractmethod
    def notify():
        pass

    @abstractmethod
    def attach():
        pass

    @abstractmethod
    def dettach():
        pass

