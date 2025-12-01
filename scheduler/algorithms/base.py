from abc import ABC, abstractmethod
from typing import List
from scheduler.process import Process

class Scheduler(ABC):
    """
    Abstract base class for all CPU scheduling algorithms.
    """

    @abstractmethod
    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Schedules the given list of processes according to the specific algorithm.

        Args:
            processes (List[Process]): A list of Process objects to be scheduled.

        Returns:
            List[Process]: The list of processes with updated simulation metrics 
                           (start_time, finish_time, waiting_time, turnaround_time).
        """
        pass
