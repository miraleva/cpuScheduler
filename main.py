from scheduler.utils.parser import parse_input
from scheduler.algorithms.fcfs import FCFS

# Input file
process = parse_input("process.txt")

# Initialize FCFS
scheduler = FCFS()
finished_process = scheduler.schedule(process)

# Print results
print("--- FCFS Results ---")
for p in finished_process:
    print(f"{p.process_id}: Finish={p.finish_time}, Turnaround={p.turnaround_time}, Waiting={p.waiting_time}")
