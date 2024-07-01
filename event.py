

class Event:

    def __init__(self, sender_id, data):
        self.sender_id = sender_id
        self.data = data

    def __str__(self):
        return (
            f"Event: sender_id={self.sender_id}, "
            f"queue_length={self.data["queue_length"]}, "
            f"state={self.data['state']} "
        )
