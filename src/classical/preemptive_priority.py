from src.classical.process import Process

def preemptive_priority_scheduling(processes):
    # Sort by arrival time for tie-breaking
    processes.sort(key=lambda x: x.arrival_time)
    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    # Make sure each process has remaining_time initialized
    for p in processes:
        p.remaining_time = p.burst_time

    while completed < n:
        index = -1
        highest_priority = float('inf')

        # Find the process with highest priority among arrived and incomplete
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i] and processes[i].remaining_time > 0:
                if processes[i].priority < highest_priority:
                    highest_priority = processes[i].priority
                    index = i
                elif processes[i].priority == highest_priority:
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
            # If no process has arrived yet or all are completed, just move time forward
            current_time += 1

    return processes

