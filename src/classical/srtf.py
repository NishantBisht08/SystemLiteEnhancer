from src.classical.process import Process

def srtf_scheduling(processes):
    # Sort by arrival time
    processes.sort(key=lambda x: x.arrival_time)

    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    while completed < n:
        index = -1
        min_remaining = float('inf') #positive infinity

        # Select process with shortest remaining time among arrived ones
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if processes[i].remaining_time < min_remaining:
                    min_remaining = processes[i].remaining_time
                    index = i
                elif processes[i].remaining_time == min_remaining:
                    if processes[i].arrival_time < processes[index].arrival_time:
                        index = i

        if index != -1:
            process = processes[index]

            # If process starts for the first time
            if process.start_time is None:
                process.start_time = current_time

            # Execute for 1 time unit (preemption possible)
            process.remaining_time -= 1
            current_time += 1

            # If process finished
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                is_completed[index] = True
                completed += 1
        else:
            # If no process has arrived yet
            current_time += 1

    return processes
