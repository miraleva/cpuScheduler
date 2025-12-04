from typing import List
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class PriorityScheduler(Scheduler):
    """
    Implementation of Priority Scheduling
    This is non-preemptive
    Lower number means higher priority
    """

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Picks the process with the highest priority (lowest number)
        
        Args:
            processes (List[Process]): The list of processes

        Returns:
            List[Process]: The processes in the order they finished
        """
        # Sort by arrival time first
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: List[Process] = []
        finished_processes: List[Process] = []
        
        current_time = 0
        
        while unarrived_processes or ready_queue:
            # Move arrived processes to the ready queue
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # If queue is empty, jump to next arrival
            if not ready_queue:
                if unarrived_processes:
                    current_time = unarrived_processes[0].arrival_time
                continue
            
            # Pick the one with the lowest priority value
            # If ties, the one that arrived first is picked automatically
            process_to_run = min(ready_queue, key=lambda p: p.priority)
            
            # Remove from queue
            ready_queue.remove(process_to_run)
            
            # Set start time
            process_to_run.start_time = current_time
            
            # Run the process
            current_time += process_to_run.burst_time
            
            # Update metrics
            process_to_run.finish_time = current_time
            process_to_run.remaining_time = 0
            process_to_run.turnaround_time = process_to_run.finish_time - process_to_run.arrival_time
            process_to_run.waiting_time = process_to_run.turnaround_time - process_to_run.burst_time
            
            finished_processes.append(process_to_run)
            
        return finished_processes
