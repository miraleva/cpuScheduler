from typing import List, Deque
from collections import deque
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class RoundRobin(Scheduler):
    """
    Round Robin (RR) scheduling algorithm.
    Preemptive.
    """

    def __init__(self, time_quantum: int):
        """
        Initialize the Round Robin scheduler with a time quantum.

        Args:
            time_quantum (int): The maximum time a process can run before preemption.
        """
        self.time_quantum = time_quantum

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Executes processes using Round Robin scheduling.
        
        Args:
            processes (List[Process]): A list of Process objects.

        Returns:
            List[Process]: The list of processes with updated metrics.
        """
        # Sort by arrival time to manage initial arrivals
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: Deque[Process] = deque()
        finished_processes: List[Process] = []
        
        current_time = 0
        
        # Keep track of processes that have been added to ready_queue to avoid duplicates
        # Actually, we pop from unarrived_processes, so no duplicates.
        
        # If there are processes, jump to the first arrival if needed
        if unarrived_processes and unarrived_processes[0].arrival_time > current_time:
            current_time = unarrived_processes[0].arrival_time

        # Initial population of ready queue
        while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
            ready_queue.append(unarrived_processes.pop(0))

        while ready_queue or unarrived_processes:
            if not ready_queue:
                # If ready queue is empty but there are still processes to arrive
                if unarrived_processes:
                    current_time = unarrived_processes[0].arrival_time
                    while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                        ready_queue.append(unarrived_processes.pop(0))
                continue

            process_to_run = ready_queue.popleft()
            
            # Set start_time if it's the first time this process runs
            if process_to_run.start_time is None:
                process_to_run.start_time = current_time
            
            # Determine how long to run
            time_slice = min(self.time_quantum, process_to_run.remaining_time)
            
            # Execute
            current_time += time_slice
            process_to_run.remaining_time -= time_slice
            
            # Check for new arrivals during this time slice
            # Note: Strictly speaking, if a process arrives exactly at current_time, 
            # it should be added.
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # Check if process finished
            if process_to_run.remaining_time == 0:
                process_to_run.finish_time = current_time
                process_to_run.turnaround_time = process_to_run.finish_time - process_to_run.arrival_time
                process_to_run.waiting_time = process_to_run.turnaround_time - process_to_run.burst_time
                finished_processes.append(process_to_run)
            else:
                # Preempted: add back to the end of the queue
                ready_queue.append(process_to_run)
                
        return finished_processes
