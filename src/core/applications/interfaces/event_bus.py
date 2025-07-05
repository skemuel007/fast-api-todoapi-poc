from abc import ABC, abstractmethod

class EventBus(ABC):
    @abstractmethod
    def publish(self, event):
        pass

    @abstractmethod
    def subscribe(self, event_type, handler):
        pass

