from abc import ABC, abstractmethod
from typing import List
from scheduler.process import Process

class Scheduler(ABC):
    """
    This is the parent class for all our schedulers
    It makes sure every algorithm has a schedule method
    """

    @abstractmethod
    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Runs the scheduling algorithm on the list of processes

        Args:
            processes (List[Process]): The processes we need to schedule

        Returns:
            List[Process]: The processes with their time metrics updated
        """
        pass
