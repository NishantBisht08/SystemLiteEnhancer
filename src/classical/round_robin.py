from src.classical.process import Process

def round_robin_scheduling(processes, time_quantum):
    n = len(processes)
    time = 0
    ready_queue = []
    remaining_burst = [p.burst_time for p in processes]
    completed = 0
    i = 0

    while completed < n:
        for p in processes:
            if p.arrival_time <= time and p not in ready_queue and remaining_burst[p.pid - 1] > 0:
                ready_queue.append(p)

        if not ready_queue:
            time += 1
            continue

        current = ready_queue.pop(0)
        exec_time = min(time_quantum, remaining_burst[current.pid - 1])
        remaining_burst[current.pid - 1] -= exec_time
        time += exec_time

        for p in processes:
            if p.arrival_time <= time and p not in ready_queue and remaining_burst[p.pid - 1] > 0:
                ready_queue.append(p)

        if remaining_burst[current.pid - 1] == 0:
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time
            completed += 1
        else:
            ready_queue.append(current)

    return processes
