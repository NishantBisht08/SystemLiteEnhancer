from src.classical.process import Process

def preemptive_priority_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    for p in processes:
        p.remaining_time = p.burst_time

    while completed < n:
        index = -1
        highest_priority = float('inf')

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
            if process.start_time is None:
                process.start_time = current_time

            process.remaining_time -= 1
            current_time += 1

            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                is_completed[index] = True
                completed += 1
        else:
            current_time += 1

    return processes


