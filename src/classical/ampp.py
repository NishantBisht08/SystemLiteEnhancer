from src.classical.process import Process
from collections import deque

def improved_mpp_scheduling(processes, quantum_base=1, aging_step=1):
    """
    Adaptive, aggressively fair, SRTF-aware MPP Scheduling.
    - Adaptive quantum: min remaining burst among READY jobs
    - SRTF within every priority group (not just RR)
    - Aggressive aging: every 'aging_step' time units
    - Immediate preempt if a process arrives that should go next
    - Should approach/better SJF/SRTF for wait/turnaround in mixed workloads
    Args:
        processes (list[Process])
        quantum_base (int): minimum quantum size
        aging_step (int): apply aging this often (lower = more aggressive)
    Returns:
        list[Process]
    """
    if not processes:
        return []
    n = len(processes)
    processes.sort(key=lambda p: (p.arrival_time, p.priority))
    current_time = 0
    completed = 0

    for p in processes:
        p.remaining_time = p.burst_time
        p.start_time = None
        p.completion_time = None
        p.turnaround_time = None
        p.waiting_time = None
        p.dynamic_priority = p.priority  # Use dynamic priority for aging

    # Priority buckets: dynamic_priority -> deque of indices
    priority_buckets = {}
    # Dynamic priority map: index --> dynamic priority
    priority_map = {i: processes[i].priority for i in range(n)}

    not_arrived = set(range(n))
    age_counter = {i: 0 for i in range(n)}  # for aging

    while completed < n:
        # Add new arrivals
        for idx in list(not_arrived):
            if processes[idx].arrival_time <= current_time:
                dyn_prio = priority_map[idx]
                priority_buckets.setdefault(dyn_prio, deque()).append(idx)
                not_arrived.remove(idx)
                age_counter[idx] = 0

        # Aging (increment all ready jobs' counters, boost frequently)
        for prio in list(priority_buckets.keys()):
            for idx in list(priority_buckets[prio]):
                if processes[idx].remaining_time > 0:
                    age_counter[idx] += 1
                    # Boost dynamically (max speed)
                    if age_counter[idx] >= aging_step and priority_map[idx] > 1:
                        # Remove from old queue
                        priority_buckets[priority_map[idx]].remove(idx)
                        priority_map[idx] -= 1
                        # Add to higher priority queue
                        priority_buckets.setdefault(priority_map[idx], deque()).appendleft(idx)
                        age_counter[idx] = 0

        # Select next runnable process:
        ready_priorities = [pr for pr in sorted(priority_buckets.keys()) if priority_buckets[pr]]
        if not ready_priorities:
            current_time += 1
            continue

        # SRTF within highest priority group
        top_prio = ready_priorities[0]
        candidates = [idx for idx in priority_buckets[top_prio] if processes[idx].remaining_time > 0]
        # Shortest remaining time among same-prio jobs
        running_idx = min(candidates, key=lambda idx: processes[idx].remaining_time)

        # Remove from queue (will add back if not done)
        priority_buckets[top_prio].remove(running_idx)
        p = processes[running_idx]

        if p.start_time is None:
            p.start_time = current_time

        # Adaptive quantum: min remaining among all ready
        ready_idxs = [i for pr in ready_priorities for i in priority_buckets[pr] if processes[i].remaining_time > 0]
        current_quantum = max(quantum_base, min([processes[i].remaining_time for i in ready_idxs+[running_idx]]))

        # Half-quantum early finish
        exec_time = (
            p.remaining_time if p.remaining_time <= current_quantum/2 else min(current_quantum, p.remaining_time)
        )

        time_run = 0
        while time_run < exec_time and p.remaining_time > 0:
            p.remaining_time -= 1
            current_time += 1
            time_run += 1
            # Add newly arriving jobs
            for idx in list(not_arrived):
                if processes[idx].arrival_time <= current_time:
                    dyn_prio = priority_map[idx]
                    priority_buckets.setdefault(dyn_prio, deque()).append(idx)
                    not_arrived.remove(idx)
                    age_counter[idx] = 0
            # Apply aging on-the-fly
            for prio in list(priority_buckets.keys()):
                for idx in list(priority_buckets[prio]):
                    if processes[idx].remaining_time > 0:
                        age_counter[idx] += 1
                        if age_counter[idx] >= aging_step and priority_map[idx] > 1:
                            priority_buckets[priority_map[idx]].remove(idx)
                            priority_map[idx] -= 1
                            priority_buckets.setdefault(priority_map[idx], deque()).appendleft(idx)
                            age_counter[idx] = 0
            # Preempt if a higher prio or same prio-shorter job arrives!
            all_ready = [
                (i, priority_map[i], processes[i].remaining_time)
                for pr in sorted(priority_buckets.keys()) for i in priority_buckets[pr] if processes[i].remaining_time > 0
            ]
            higher = [x for x in all_ready if x[1] < priority_map[running_idx]]
            shorter_same = [
                x for x in all_ready if x[1] == priority_map[running_idx]
                and x[2] < p.remaining_time
            ]
            if higher or shorter_same:
                break  # Preempt on better

        # Mark complete or requeue
        if p.remaining_time == 0:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed += 1
        else:
            # Not finished: back into dynamic queue, SRTF keeps it fair
            priority_buckets.setdefault(priority_map[running_idx], deque()).append(running_idx)

    return processes
