from typing import List, Deque, Tuple, Union, Optional
from collections import deque
from scheduler.process import Process
from scheduler.algorithms.base import Scheduler

class RoundRobin(Scheduler):
    """
    Round Robin (RR) scheduling algorithm with Context Switching.
    Preemptive.
    """

    def __init__(self, time_quantum: int, context_switch_time: int = 0):
        """
        Initialize the Round Robin scheduler.

        Args:
            time_quantum (int): The maximum time a process can run before preemption.
            context_switch_time (int): Time taken to switch between processes.
        """
        self.time_quantum = time_quantum
        self.context_switch_time = context_switch_time

    def schedule(self, processes: List[Process]) -> Tuple[List[Process], List[Tuple[int, Union[str, int], int]]]:
        """
        Executes processes using Round Robin scheduling with context switches.
        
        Args:
            processes (List[Process]): A list of Process objects.

        Returns:
            Tuple[List[Process], List[Tuple]]: 
                - List of finished processes with updated metrics.
                - Gantt chart list of tuples (start_time, process_id_or_CS, end_time).
        """
        # Sort by arrival time
        unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue: Deque[Process] = deque()
        finished_processes: List[Process] = []
        gantt_chart: List[Tuple[int, Union[str, int], int]] = []
        
        current_time = 0
        last_process_id: Optional[int] = None
        
        # Initial population of ready queue
        # If no processes arrive at 0, jump to first arrival
        if unarrived_processes and unarrived_processes[0].arrival_time > current_time:
            current_time = unarrived_processes[0].arrival_time
            
        while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
            ready_queue.append(unarrived_processes.pop(0))

        while ready_queue or unarrived_processes:
            if not ready_queue:
                # Idle time
                if unarrived_processes:
                    next_arrival = unarrived_processes[0].arrival_time
                    # Record idle time in Gantt if desired, or just jump
                    # gantt_chart.append((current_time, "IDLE", next_arrival))
                    current_time = next_arrival
                    while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                        ready_queue.append(unarrived_processes.pop(0))
                continue

            process_to_run = ready_queue.popleft()
            
            # Context Switch Check
            # We incur context switch if there was a previous process and it's different from current
            # OR if it's the same process but it was preempted and re-scheduled (technically implementation dependent, 
            # but usually CS happens on any scheduler invocation that swaps context. 
            # Requirements say "every time the CPU switches to a different process".
            # So if P1 runs, gets preempted, and P1 runs again immediately (only one in queue), no CS?
            # Usually RR with 1 process doesn't CS.
            # If P1 -> P2, yes CS.
            if last_process_id is not None and process_to_run.process_id != last_process_id:
                if self.context_switch_time > 0:
                    start_cs = current_time
                    current_time += self.context_switch_time
                    gantt_chart.append((start_cs, "CS", current_time))
            
            # Update start time if first run
            if process_to_run.start_time is None:
                process_to_run.start_time = current_time
            
            # Execute
            time_slice = min(self.time_quantum, process_to_run.remaining_time)
            start_exec = current_time
            current_time += time_slice
            process_to_run.remaining_time -= time_slice
            
            # Record execution in Gantt
            gantt_chart.append((start_exec, process_to_run.process_id, current_time))
            
            last_process_id = process_to_run.process_id
            
            # Check for new arrivals
            while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
                ready_queue.append(unarrived_processes.pop(0))
            
            # Check if finished
            if process_to_run.remaining_time == 0:
                process_to_run.finish_time = current_time
                process_to_run.turnaround_time = process_to_run.finish_time - process_to_run.arrival_time
                process_to_run.waiting_time = process_to_run.turnaround_time - process_to_run.burst_time
                finished_processes.append(process_to_run)
            else:
                # Preempted
                ready_queue.append(process_to_run)
                
        return finished_processes, gantt_chart
