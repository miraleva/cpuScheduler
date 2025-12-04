import sys
from scheduler.utils.parser import parse_input
from scheduler.algorithms.fcfs import FCFS
from scheduler.algorithms.sjf import SJF
from scheduler.algorithms.priority import PriorityScheduler
from scheduler.algorithms.round_robin import RoundRobin

if len(sys.argv) < 3:
    print("Usage: python main.py <input_file> <algorithm> [time_quantum] [context_switch]")
    sys.exit(1)

input_file = sys.argv[1]
algorithm = sys.argv[2].lower()
time_quantum = int(sys.argv[3]) if len(sys.argv) > 3 else None
context_switch = int(sys.argv[4]) if len(sys.argv) > 4 else 0

# Read the input file
processes = parse_input(input_file)

# Pick the right scheduler based on user input
if algorithm == "fcfs":
    scheduler = FCFS()
elif algorithm == "sjf":
    scheduler = SJF()
elif algorithm == "priority":
    scheduler = PriorityScheduler()
elif algorithm == "rr":
    if time_quantum is None:
        print("Error: Time quantum is required for Round Robin")
        sys.exit(1)
    scheduler = RoundRobin(time_quantum, context_switch)
else:
    print(f"Unknown algorithm: {algorithm}")
    sys.exit(1)

# Run the scheduler
if algorithm == "rr":
    finished_processes, gantt_chart = scheduler.schedule(processes)
    # Print the Gantt Chart for RR
    print("--- Gantt Chart ---")
    gantt_str = ""
    for start, pid, end in gantt_chart:
        gantt_str += f"[{start}]-{pid}-[{end}]-"
    print(gantt_str[:-1]) # Remove the last dash
else:
    finished_processes = scheduler.schedule(processes)

# Print the table of results
print(f"--- {algorithm.upper()} Results ---")
print("PID | Arrival | Burst | Start | Finish | Waiting | Turnaround")
total_waiting = 0
total_turnaround = 0
max_finish_time = 0
min_arrival_time = float('inf')
total_burst = 0

for p in finished_processes:
    print(f"{p.process_id:>3} | {p.arrival_time:>7} | {p.burst_time:>5} | "
          f"{p.start_time:>5} | {p.finish_time:>6} | {p.waiting_time:>7} | {p.turnaround_time:>10}")
    total_waiting += p.waiting_time
    total_turnaround += p.turnaround_time
    total_burst += p.burst_time
    if p.finish_time > max_finish_time:
        max_finish_time = p.finish_time
    if p.arrival_time < min_arrival_time:
        min_arrival_time = p.arrival_time

# Calculate averages
n = len(finished_processes)
if n > 0:
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n
    
    # CPU Utilization = Total time spent working / Total time passed
    total_time = max_finish_time
    cpu_utilization = (total_burst / total_time) * 100 if total_time > 0 else 0

    print("-" * 60)
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
