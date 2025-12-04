from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:
    """
    Holds all the details for a single process
    
    Attributes:
        process_id (int): The ID of the process
        arrival_time (int): When the process arrives
        burst_time (int): How long the process needs to run
        priority (int): The priority value (lower might mean more important)
        remaining_time (int): How much time is left to finish
        start_time (Optional[int]): When the process started running
        finish_time (Optional[int]): When the process finished running
        waiting_time (int): How long the process waited in the queue
        turnaround_time (int): Total time from arrival to finish
    """
    # Input fields from the file
    process_id: int
    arrival_time: int
    burst_time: int
    priority: int

    # Fields we calculate during simulation
    remaining_time: int = 0
    start_time: Optional[int] = None
    finish_time: Optional[int] = None
    waiting_time: int = 0
    turnaround_time: int = 0

    def __post_init__(self):
        """Set the initial remaining time to the full burst time"""
        self.remaining_time = self.burst_time
