from src.classical.process import Process
from collections import deque

def mpp_scheduling(processes):
    """
    Modified Priority Preemptive (MPP) CPU Scheduling
    Based on the research paper:
    - Priority-grouped Round Robin scheduling
    - Time Quantum Q = minimum burst time among all processes
    - Half Quantum rule: If remaining_time <= Q/2 → finish immediately
    - Prevents starvation & reduces waiting/turnaround time
    
    Args:
        processes (list[Process])
    Returns:
        list[Process]: with updated CT, TAT, WT
    """

    if not processes:
        return []

    # Sort by arrival time first
    processes.sort(key=lambda p: p.arrival_time)

    n = len(processes)
    current_time = 0
    completed = 0

    # Ensure remaining_time is set
    for p in processes:
        p.remaining_time = p.burst_time
        p.start_time = None

    # Q = shortest burst time of all processes (paper definition)
    Q = min(p.burst_time for p in processes)

    # Create priority buckets (priority → queue of indices)
    priority_buckets = {}
    for i, p in enumerate(processes):
        priority_buckets.setdefault(p.priority, deque())
    
    # Track processes not yet arrived
    not_arrived = set(range(n))

    # Keep priority list sorted (lower number = higher priority)
    sorted_priorities = sorted(priority_buckets.keys())

    while completed < n:

        # Add newly arrived processes to their priority bucket
        arrived_now = []
        for idx in list(not_arrived):
            if processes[idx].arrival_time <= current_time:
                priority_buckets[processes[idx].priority].append(idx)
                arrived_now.append(idx)
                not_arrived.remove(idx)

        # If nothing is available → move time forward
        if all(len(priority_buckets[p]) == 0 for p in sorted_priorities):
            current_time += 1
            continue

        # ----------------------------
        # Priority-group Round Robin
        # Pick first non-empty priority queue
        # ----------------------------
        running_idx = None
        running_priority = None

        for pr in sorted_priorities:
            if priority_buckets[pr]:
                running_idx = priority_buckets[pr].popleft()
                running_priority = pr
                break

        p = processes[running_idx]

        # First time execution marking
        if p.start_time is None:
            p.start_time = current_time

        # HALF QUANTUM RULE
        if p.remaining_time <= Q / 2:
            exec_time = p.remaining_time   # finish immediately
        else:
            exec_time = min(Q, p.remaining_time)

        # Execute process
        p.remaining_time -= exec_time
        current_time += exec_time

        # Check arrivals during execution
        for idx in list(not_arrived):
            if processes[idx].arrival_time <= current_time:
                priority_buckets[processes[idx].priority].append(idx)
                not_arrived.remove(idx)

        # Completion?
        if p.remaining_time == 0:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed += 1
        else:
            # Preempt & push back at end of its priority bucket (RR behavior)
            priority_buckets[running_priority].append(running_idx)

    return processes
