import random

# ==========================================================
# Dynamic Round Robin (Arrival Time = 0 for all processes)
# ==========================================================

def drr0_scheduling(processes):
    """
    processes: list of Process objects imported from process.py
    """

    n = len(processes)

    # Extract burst times & arrival times (all AT = 0)
    burst_times = [p.burst_time for p in processes]
    arrival_times = [0] * n

    # Internal state
    rem_bt = burst_times.copy()
    time = 0
    completed = 0
    tq = 4  # initial TQ

    # Output arrays
    waiting_time = [0] * n
    turnaround_time = [0] * n
    response_time = [-1] * n

    gantt = []  # (pid, start, end)
    ready = []

    # Put all processes instantly in ready queue
    ready = list(range(n))  # since arrival = 0 for all

    while completed != n:
        if not ready:
            time += 1
            continue

        i = ready.pop(0)  # index of the process

        # Response time for first CPU allocation
        if response_time[i] == -1:
            response_time[i] = time

        # CPU Execution
        exec_time = min(rem_bt[i], tq)
        gantt.append((processes[i].pid, time, time + exec_time))

        time += exec_time
        rem_bt[i] -= exec_time

        if rem_bt[i] == 0:  # Process finished
            completed += 1
            turnaround_time[i] = time  # since AT = 0 → TAT = completion time
            waiting_time[i] = turnaround_time[i] - burst_times[i]
        else:
            # Still remaining → put back to queue
            ready.append(i)

        # Update TQ dynamically
        remaining_bt = [x for x in rem_bt if x > 0]
        if remaining_bt:
            tq = (sum(remaining_bt) // len(remaining_bt)) + 1
            tq = max(2, min(tq, 25))  # bound TQ

    # Update Process objects
    for i in range(n):
        processes[i].waiting_time = waiting_time[i]
        processes[i].turnaround_time = turnaround_time[i]
        processes[i].start_time = response_time[i]
        processes[i].completion_time = turnaround_time[i]

    return processes  # must return updated process list

