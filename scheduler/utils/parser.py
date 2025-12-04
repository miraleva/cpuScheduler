from typing import List
from scheduler.process import Process

def parse_input(file_path: str) -> List[Process]:
    """
    Reads the process data from the text file
    
    The file should look like this:
    Process_ID, Arrival_Time, Burst_Time, Priority

    Args:
        file_path (str): Where the file is located

    Returns:
        List[Process]: A list of Process objects we created
    """
    processes: List[Process] = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            
            # Split the line by commas
            parts = line.split(',')
            
            # Convert strings to integers
            pid = int(parts[0].strip())
            arrival = int(parts[1].strip())
            burst = int(parts[2].strip())
            priority = int(parts[3].strip())
            
            # Create a new Process object and add it to our list
            processes.append(Process(
                process_id=pid,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
            
    return processes
