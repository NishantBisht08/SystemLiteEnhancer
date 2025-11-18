# Dynamic Round Robin Scheduling (Varied Arrival Time Compatible)

def drr_scheduling(processes, initial_tq=4):
    # Sort by arrival time
    processes = sorted(processes, key=lambda p: p.arrival_time)
    time = 0
    completed = 0
    tq = initial_tq
    n = len(processes)
    ready = []
    gantt = []
    p.remaining_time = p.burst_time
    p.start_time = None
    def update_ready():
        for p in processes:
        if p.arrival_time <= time and p.remaining_time > 0 and p not in ready:
        ready.append(p)
    update_ready()
    while completed != n:
    if not ready:
     time += 1
    update_ready()
    continue
    p = ready.pop(0)
    if p.start_time is None:
    p.start_time = time
    exec_time = min(p.remaining_time, tq)
    gantt.append((p.pid, time, time + exec_time))
    time += exec_time
    p.remaining_time -= exec_time
    if p.remaining_time == 0:
    completed += 1
    p.completion_time = time
    p.turnaround_time = p.completion_time - p.arrival_time
    p.waiting_time = p.turnaround_time - p.burst_time
    else:
    update_ready()
    ready.append(p)
    update_ready()
    remaining = [x.remaining_time for x in processes if x.remaining_time > 0]
    if remaining:
    tq = (sum(remaining) // len(remaining)) + 1
    tq = max(2, min(tq, 25))
     return processes
# Dynamic Round Robin Scheduling (Varied Arrival Time Compatible)
    def drr_scheduling(processes, initial_tq=4):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    time = 0
    completed = 0
    tq = initial_tq
    n = len(processes)
     ready = []
    gantt = []
    for p in processes:
    p.remaining_time = p.burst_time
    p.start_time = None
    def update_ready():
        for p in processes:
        if p.arrival_time <= time and p.remaining_time > 0 and p not in ready:
        ready.append(p)
    update_ready()
    while completed != n:
    if not ready:
    time += 1
    update_ready()
    continue
    p = ready.pop(0)
    if p.start_time is None:
    p.start_time = time
    exec_time = min(p.remaining_time, tq)
    gantt.append((p.pid, time, time + exec_time))
    time += exec_time
    p.remaining_time -= exec_time
    if p.remaining_time == 0:
    completed += 1
    p.completion_time = time
    p.turnaround_time = p.completion_time - p.arrival_time
    p.waiting_time = p.turnaround_time - p.burst_time
    else:
    update_ready()
    ready.append(p)
    update_ready()
    remaining = [x.remaining_time for x in processes if x.remaining_time > 0]
    if remaining:
    tq = (sum(remaining) // len(remaining)) + 1
    tq = max(2, min(tq, 25))
    return processes
