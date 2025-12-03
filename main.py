import sys
from scheduler.utils.parser import parse_input
from scheduler.algorithms.fcfs import FCFS
from scheduler.algorithms.sjf import SJF
from scheduler.algorithms.priority import PriorityScheduler
from scheduler.algorithms.round_robin import RoundRobin

if len(sys.argv) < 3:
    print("Usage: python main.py <input_file> <algorithm> [time_quantum_for_RR]")
    sys.exit(1)

input_file = sys.argv[1]
algorithm = sys.argv[2].lower()
time_quantum = int(sys.argv[3]) if len(sys.argv) > 3 else None

# Input dosyasını oku
processes = parse_input(input_file)

# Scheduler seçimi
if algorithm == "fcfs":
    scheduler = FCFS()
elif algorithm == "sjf":
    scheduler = SJF()
elif algorithm == "priority":
    scheduler = PriorityScheduler()
elif algorithm == "rr":
    if time_quantum is None:
        print("Error: Time quantum is required for Round Robin.")
        sys.exit(1)
    scheduler = RoundRobin(time_quantum)
else:
    print(f"Unknown algorithm: {algorithm}")
    sys.exit(1)

# Çalıştır
finished_processes = scheduler.schedule(processes)

# Sonuçları yazdır
print(f"--- {algorithm.upper()} Results ---")
print("PID | Arrival | Burst | Start | Finish | Waiting | Turnaround")
for p in finished_processes:
    print(f"{p.process_id:>3} | {p.arrival_time:>7} | {p.burst_time:>5} | "
          f"{p.start_time:>5} | {p.finish_time:>6} | {p.waiting_time:>7} | {p.turnaround_time:>10}")
