from utils.publishers.opportunity_publisher import OpportunityPublisher
from utils.send_email import send_email


class OpportunityObserver:
    """Notifies subscribers about new internships
        and new job alerts
    """

    @classmethod
    def handle_new_internship(cls, event_type: str, batches: list[int]):
        """Notifies subscribers about new internship."""
        
        pass

    @classmethod
    def handle_new_job(cls, event_type: str, batches: list[int]):
        """Notifies subscribers about new job."""

        pass

    @staticmethod
    def setup(cls):
        """Sets up observer for subscriptions to events"""

        OpportunityPublisher.attach("new_internship", 
        OpportunityObserver.handle_new_internship)

        OpportunityPublisher.attach("new_job", 
        OpportunityObserver.handle_new_job)
