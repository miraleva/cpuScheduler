from typing import List
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class SJF(Scheduler):
    """
    Shortest Job First (SJF) scheduling algorithm.
    Non-preemptive.
    """

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Executes processes based on the shortest burst time.
        Non-preemptive: Once a process starts, it runs to completion.
        Tie-breaking: FCFS (Arrival Time).
        
        Args:
            processes (List[Process]): A list of Process objects.

        Returns:
            List[Process]: The list of processes with updated metrics, ordered by finish time.
        """
        # Working with a copy of the list to avoid modifying the original list order immediately,
        # though we will modify the objects themselves.
        # Sort unarrived processes by arrival time initially to manage the timeline.
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: List[Process] = []
        finished_processes: List[Process] = []
        
        current_time = 0
        
        # Continue until all processes are finished
        while unarrived_processes or ready_queue:
            # Move all processes that have arrived by current_time to the ready queue
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # If no process is ready, jump to the next arrival time (idle CPU)
            if not ready_queue:
                if unarrived_processes:
                    current_time = unarrived_processes[0].arrival_time
                continue
            
            # Select the process with the smallest burst time.
            # Python's min() is stable; since ready_queue is populated in arrival order,
            # ties in burst_time are broken by arrival order (FCFS).
            process_to_run = min(ready_queue, key=lambda p: p.burst_time)
            
            # Remove the selected process from the ready queue
            ready_queue.remove(process_to_run)
            
            # Update start time (it might be the first time it starts)
            # Since it's non-preemptive, start_time is simply current_time
            process_to_run.start_time = current_time
            
            # Update current time by adding burst time (execution)
            current_time += process_to_run.burst_time
            
            # Update finish time and other metrics
            process_to_run.finish_time = current_time
            process_to_run.remaining_time = 0
            process_to_run.turnaround_time = process_to_run.finish_time - process_to_run.arrival_time
            process_to_run.waiting_time = process_to_run.turnaround_time - process_to_run.burst_time
            
            finished_processes.append(process_to_run)
            
        return finished_processes
