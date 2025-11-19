# python -m tests.python_test_schedulers
from src.classical.process import Process
from src.classical.fcfs import fcfs_scheduling
from src.classical.sjf import sjf_scheduling
from src.classical.nonpreemtive_priority import priority_scheduling
from src.classical.srtf import srtf_scheduling
from src.classical.preemptive_priority import preemptive_priority_scheduling
from src.classical.round_robin import round_robin_scheduling
from src.classical.mpp import mpp_scheduling
from src.classical.drr0 import drr0_scheduling
from src.classical.drr import drr_scheduling
from src.classical.ampp import improved_mpp_scheduling
from tests.input_fixed_30 import get_fixed_30_processes

import matplotlib.pyplot as plt

def print_results(processes, algorithm_name):
    print(f"\nResults for {algorithm_name}:")
    print("PID\tArrival\tBurst\tPriority\tWaiting\tTurnaround")
    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.priority}\t\t{p.waiting_time}\t{p.turnaround_time}")

def print_stats(processes, algorithm_name):
    n = len(processes)
    avg_waiting = sum(p.waiting_time for p in processes) / n
    avg_turnaround = sum(p.turnaround_time for p in processes) / n
    throughput = n / max(p.completion_time for p in processes)
    print(f"\nStats for {algorithm_name}:")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Throughput: {throughput:.2f} processes/unit time")

def print_complete_metrics(processes, algorithm_name):
    n = len(processes)
    burst_sum = sum(p.burst_time for p in processes)
    earliest_arrival = min(p.arrival_time for p in processes)
    finish_time = max(p.completion_time for p in processes)
    avg_waiting = sum(p.waiting_time for p in processes) / n
    avg_turnaround = sum(p.turnaround_time for p in processes) / n
    max_waiting = max(p.waiting_time for p in processes)
    waiting_times = [p.waiting_time for p in processes]
    turnaround_times = [p.turnaround_time for p in processes]
    waiting_variance = sum((wt - avg_waiting) ** 2 for wt in waiting_times) / n
    tat_avg = avg_turnaround
    tat_variance = sum((tat - tat_avg) ** 2 for tat in turnaround_times) / n

    start_times = sorted([p.start_time for p in processes if p.start_time is not None])
    idle_time = 0
    if start_times:
        idle_time = max(0, start_times[0] - earliest_arrival)
        for i in range(1, len(start_times)):
            prev_completion = max(p.completion_time for p in processes if p.start_time == start_times[i-1])
            idle_time += max(0, start_times[i] - prev_completion)
    cpu_util = 100 * burst_sum / (burst_sum + idle_time) if (burst_sum + idle_time) > 0 else 0
    throughput = n / (finish_time - earliest_arrival) if finish_time - earliest_arrival > 0 else 0

    print(f"\nComplete Metrics for {algorithm_name}:")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Maximum Waiting Time: {max_waiting}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Waiting Time Variance: {waiting_variance:.2f}")
    print(f"Turnaround Time Variance: {tat_variance:.2f}")
    print(f"CPU Utilization: {cpu_util:.2f}%")
    print(f"System Idle Time: {idle_time}")
    print(f"Throughput: {throughput:.2f} processes/unit time")

def get_initial_processes():
    # Always returns fresh list of Process objects
    return [
        Process(pid=1, burst_time=6, priority=2, arrival_time=1),
        Process(pid=2, burst_time=8, priority=1, arrival_time=1),
        Process(pid=3, burst_time=7, priority=3, arrival_time=2),
        Process(pid=4, burst_time=3, priority=2, arrival_time=3),
    ]

def copy_processes(processes):
    """Return new Process instances with original fields (fresh for each algorithm)."""
    return [
        Process(pid=p.pid, burst_time=p.burst_time, priority=p.priority, arrival_time=p.arrival_time)
        for p in processes
    ]
    
def plot_metrics(results_data):
    algos = [r['algo'] for r in results_data]
    avg_waits = [r['avg_wait'] for r in results_data]
    avg_tats = [r['avg_tat'] for r in results_data]

    plt.bar(algos, avg_waits, color='dodgerblue')
    plt.title('Average Waiting Time (4 Processes)')
    plt.xlabel('Algorithm')
    plt.ylabel('Average Waiting')
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()

    plt.bar(algos, avg_tats, color='orange')
    plt.title('Average Turnaround Time (4 Processes)')
    plt.xlabel('Algorithm')
    plt.ylabel('Average Turnaround')
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()

def main():
    results_data_4 = []
    # === 4-process fixed input ===
    print("\n====== Results for 4 Fixed Processes ======")
    for name, sched, kwargs in [
        ("FCFS", fcfs_scheduling, {}),
        ("SJF", sjf_scheduling, {}),
        ("Priority", priority_scheduling, {}),
        ("SRTF", srtf_scheduling, {}),
        ("Preemptive Priority", preemptive_priority_scheduling, {}),
        ("Round Robin", round_robin_scheduling, {'time_quantum':2}),
        ("MPP", mpp_scheduling, {}),
        ("DRR0", drr0_scheduling, {}),
        ("DRR", drr_scheduling, {'initial_tq':4}),
        ("AMPP", improved_mpp_scheduling, {})
    ]:
        procs = get_initial_processes()
        result = sched(procs, **kwargs) if kwargs else sched(procs)
        print_results(result, name)
        print_stats(result, name)
        print_complete_metrics(result, name)
        
        avg_waiting = sum(p.waiting_time for p in result) / len(result)
        avg_turnaround = sum(p.turnaround_time for p in result) / len(result)
        results_data_4.append({'algo': name, 'avg_wait': avg_waiting, 'avg_tat': avg_turnaround})

    # Plot only for 4 processes
    plot_metrics(results_data_4)
    
    # === 30-process fixed input from separate file ===
    print("\n====== Results for 30 Fixed Processes ======")
    fixed_30 = get_fixed_30_processes()
    for name, sched, kwargs in [
        ("FCFS", fcfs_scheduling, {}),
        ("SJF", sjf_scheduling, {}),
        ("Priority", priority_scheduling, {}),
        ("SRTF", srtf_scheduling, {}),
        ("Preemptive Priority", preemptive_priority_scheduling, {}),
        ("Round Robin", round_robin_scheduling, {'time_quantum':2}),
        ("MPP", mpp_scheduling, {}),
        ("DRR0", drr0_scheduling, {}),
        ("DRR", drr_scheduling, {'initial_tq':4}),
        ("AMPP", improved_mpp_scheduling, {})
    ]:
        procs = copy_processes(fixed_30)
        result = sched(procs, **kwargs) if kwargs else sched(procs)
        print_results(result, f"{name} (30 Fixed)")
        print_stats(result, f"{name} (30 Fixed)")
        print_complete_metrics(result, f"{name} (30 Fixed)")
        # (Optionally save 30-process stats in a different list if wanted)

if __name__ == "__main__":
    main()





