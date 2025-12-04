from typing import List
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class FCFS(Scheduler):
    """
    Implementation of First-Come First-Served algorithm
    This is non-preemptive, meaning once a process starts, it finishes
    """

    def schedule(self, processes: List[Process]) -> List[Process]:
        """
        Runs processes in the order they arrived
        
        Args:
            processes (List[Process]): The list of processes

        Returns:
            List[Process]: The updated processes
        """
        # Sort the processes by arrival time so the first one comes first
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        current_time = 0
        
        for process in sorted_processes:
            # If the CPU is free but the process hasn't arrived yet, we wait
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # The process starts now
            process.start_time = current_time
            
            # It runs for the full burst time
            current_time += process.burst_time
            
            # The process is done
            process.finish_time = current_time
            process.remaining_time = 0
            
            # Calculate the stats
            process.turnaround_time = process.finish_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
        return sorted_processes
