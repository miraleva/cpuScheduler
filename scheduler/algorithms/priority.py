from typing import List
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class PriorityScheduler(Scheduler):
    """
    Priority scheduling algorithm (Non-preemptive).
    Lower priority value indicates higher priority.
    """

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Executes processes based on priority.
        Non-preemptive: Once a process starts, it runs to completion.
        Tie-breaking: FCFS (Arrival Time).
        
        Args:
            processes (List[Process]): A list of Process objects.

        Returns:
            List[Process]: The list of processes with updated metrics, ordered by finish time.
        """
        # Sort unarrived processes by arrival time initially
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: List[Process] = []
        finished_processes: List[Process] = []
        
        current_time = 0
        
        while unarrived_processes or ready_queue:
            # Move all processes that have arrived by current_time to the ready queue
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # If no process is ready, jump to the next arrival time (idle CPU)
            if not ready_queue:
                if unarrived_processes:
                    current_time = unarrived_processes[0].arrival_time
                continue
            
            # Select the process with the highest priority (lowest value).
            # Tie-breaking: If priorities are equal, pick the one that arrived earlier.
            # Since ready_queue is populated in arrival order, min() will pick the first occurrence
            # of the minimum priority, preserving FCFS for ties.
            process_to_run = min(ready_queue, key=lambda p: p.priority)
            
            # Remove the selected process from the ready queue
            ready_queue.remove(process_to_run)
            
            # Update start time
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
