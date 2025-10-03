from src.classical.process import Process

def sjf_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    while completed < n:
        idx = -1
        min_burst = float('inf')

        for i in range(n):
            if (processes[i].arrival_time <= current_time) and (not is_completed[i]):
                if processes[i].burst_time < min_burst:
                    min_burst = processes[i].burst_time
                    idx = i
                elif processes[i].burst_time == min_burst:
                    if processes[i].arrival_time < processes[idx].arrival_time:
                        idx = i

        if idx != -1:
            process = processes[idx]
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1

    return processes
