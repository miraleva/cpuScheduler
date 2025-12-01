from typing import List
from scheduler.process import Process

def parse_input(file_path: str) -> List[Process]:
    """
    Reads an input file and parses process information.

    The expected file format is CSV-like or space-separated:
    Process_ID, Arrival_Time, Burst_Time, Priority

    Args:
        file_path (str): The path to the input file.

    Returns:
        List[Process]: A list of Process objects parsed from the file.
    """
    processes: List[Process] = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split by comma (assuming CSV format based on requirements)
            parts = line.split(',')
            
            # Basic parsing without validation as requested
            pid = int(parts[0].strip())
            arrival = int(parts[1].strip())
            burst = int(parts[2].strip())
            priority = int(parts[3].strip())
            
            processes.append(Process(
                process_id=pid,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
            
    return processes
