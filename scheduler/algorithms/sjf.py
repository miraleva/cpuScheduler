from typing import List
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class SJF(Scheduler):
    """
    Implementation of Shortest Job First (SJF)
    This is non-preemptive, so we pick the shortest job and run it fully
    """

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Picks the process with the smallest burst time from the ready queue
        
        Args:
            processes (List[Process]): The list of processes

        Returns:
            List[Process]: The processes in the order they finished
        """
        # We sort by arrival time first to handle them easily
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: List[Process] = []
        finished_processes: List[Process] = []
        
        current_time = 0
        
        # Keep going until we have processed everyone
        while unarrived_processes or ready_queue:
            # Add everyone who has arrived by now to the ready queue
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # If nobody is ready, we jump to the next arrival time
            if not ready_queue:
                if unarrived_processes:
                    current_time = unarrived_processes[0].arrival_time
                continue
            
            # Find the process with the smallest burst time
            # If there is a tie, min() picks the one that came first (stable sort)
            process_to_run = min(ready_queue, key=lambda p: p.burst_time)
            
            # Remove it from the queue because we are going to run it
            ready_queue.remove(process_to_run)
            
            # It starts now
            process_to_run.start_time = current_time
            
            # It runs for the full burst time
            current_time += process_to_run.burst_time
            
            # Update all the metrics
            process_to_run.finish_time = current_time
            process_to_run.remaining_time = 0
            process_to_run.turnaround_time = process_to_run.finish_time - process_to_run.arrival_time
            process_to_run.waiting_time = process_to_run.turnaround_time - process_to_run.burst_time
            
            finished_processes.append(process_to_run)
            
        return finished_processes
