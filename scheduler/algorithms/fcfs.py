from typing import List
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class FCFS(Scheduler):
    """
    First-Come First-Served (FCFS) scheduling algorithm.
    Non-preemptive.
    """

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Executes processes in the order of their arrival time.
        
        Args:
            processes (List[Process]): A list of Process objects.

        Returns:
            List[Process]: The list of processes with updated metrics.
        """
        # Sort by arrival time. FCFS tie-breaking is implicit in stable sort or arrival order.
        # If arrival times are equal, we can use process ID or original order as tie-breaker.
        # Python's sort is stable, so original order is preserved for ties.
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        
        for process in sorted_processes:
            # If the CPU is idle until this process arrives
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Process starts execution
            process.start_time = current_time
            
            # Process runs for its full burst time (non-preemptive)
            current_time += process.burst_time
            
            # Process finishes
            process.finish_time = current_time
            process.remaining_time = 0
            
            # Calculate metrics
            process.turnaround_time = process.finish_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
        return sorted_processes
