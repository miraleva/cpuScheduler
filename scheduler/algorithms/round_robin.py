from typing import List, Deque, Tuple, Union, Optional
from collections import deque
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class RoundRobin(Scheduler):
    """
    Implementation of Round Robin (RR)
    This is preemptive, so processes take turns
    We also handle context switching here
    """

    def __init__(self, time_quantum: int, context_switch_time: int = 0):
        """
        Setup the scheduler

        Args:
            time_quantum (int): Max time a process runs at once
            context_switch_time (int): Time lost when switching processes
        """
        self.time_quantum = time_quantum
        self.context_switch_time = context_switch_time

    def schedule(self, processes: List[Process]) -> Tuple[List[Process], List[Tuple[int, Union[str, int], int]]]:
        """
        Runs the Round Robin logic
        
        Args:
            processes (List[Process]): The list of processes

        Returns:
            Tuple: A list of finished processes and the Gantt chart data
        """
        # Sort by arrival time
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: Deque[Process] = deque()
        finished_processes: List[Process] = []
        gantt_chart: List[Tuple[int, Union[str, int], int]] = []
        
        current_time = 0
        last_process_id: Optional[int] = None
        
        # If the first process doesn't arrive at 0, we jump ahead
        if unarrived_processes and unarrived_processes[0].arrival_time > current_time:
            current_time = unarrived_processes[0].arrival_time
            
        # Add initial processes to the queue
        while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
            ready_queue.append(unarrived_processes.pop(0))

        while ready_queue or unarrived_processes:
            if not ready_queue:
                # If queue is empty, we wait for the next process
                if unarrived_processes:
                    next_arrival = unarrived_processes[0].arrival_time
                    current_time = next_arrival
                    while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                        ready_queue.append(unarrived_processes.pop(0))
                continue

            process_to_run = ready_queue.popleft()
            
            # Handle Context Switch
            # If we are switching to a different process, we add the overhead
            if last_process_id is not None and process_to_run.process_id != last_process_id:
                if self.context_switch_time > 0:
                    start_cs = current_time
                    current_time += self.context_switch_time
                    gantt_chart.append((start_cs, "CS", current_time))
            
            # If this is the first time it runs, save the start time
            if process_to_run.start_time is None:
                process_to_run.start_time = current_time
            
            # Decide how long to run (either full quantum or just what's left)
            time_slice = min(self.time_quantum, process_to_run.remaining_time)
            start_exec = current_time
            current_time += time_slice
            process_to_run.remaining_time -= time_slice
            
            # Add this run to the Gantt chart
            gantt_chart.append((start_exec, process_to_run.process_id, current_time))
            
            last_process_id = process_to_run.process_id
            
            # Check if any new processes arrived while we were running
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # Check if the process is finished
            if process_to_run.remaining_time == 0:
                process_to_run.finish_time = current_time
                process_to_run.turnaround_time = process_to_run.finish_time - process_to_run.arrival_time
                process_to_run.waiting_time = process_to_run.turnaround_time - process_to_run.burst_time
                finished_processes.append(process_to_run)
            else:
                # If not finished, it goes back to the end of the line
                ready_queue.append(process_to_run)
                
        return finished_processes, gantt_chart
