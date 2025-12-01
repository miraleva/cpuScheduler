from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:
    """
    Represents a process in the CPU scheduling simulator.
    
    Attributes:
        process_id (int): Unique identifier for the process.
        arrival_time (int): Time at which the process arrives in the ready queue.
        burst_time (int): Total CPU time required by the process.
        priority (int): Priority of the process (lower value might imply higher priority, depending on algorithm).
        remaining_time (int): Remaining CPU time needed to complete execution.
        start_time (Optional[int]): Time when the process first gets the CPU. None if not yet started.
        finish_time (Optional[int]): Time when the process completes execution. None if not yet finished.
        waiting_time (int): Total time spent in the ready queue.
        turnaround_time (int): Total time from arrival to completion.
    """
    # Input fields
    process_id: int
    arrival_time: int
    burst_time: int
    priority: int

    # Simulation fields
    remaining_time: int = 0
    start_time: Optional[int] = None
    finish_time: Optional[int] = None
    waiting_time: int = 0
    turnaround_time: int = 0

    def __post_init__(self):
        """Initialize remaining_time to burst_time upon creation."""
        self.remaining_time = self.burst_time
