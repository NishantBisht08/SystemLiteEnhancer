#python -m tests.python_test_schedulers
from src.classical.process import Process
from src.classical.fcfs import fcfs_scheduling
from src.classical.sjf import sjf_scheduling
from src.classical.nonpreemtive_priority import priority_scheduling
from src.classical.srtf import srtf_scheduling
from src.classical.preemptive_priority import preemptive_priority_scheduling
from src.classical.round_robin import round_robin_scheduling



def print_results(processes, algorithm_name):
    print(f"\nResults for {algorithm_name}:")
    print("PID\tArrival\tBurst\tPriority\tWaiting\tTurnaround")
    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.priority}\t\t{p.waiting_time}\t{p.turnaround_time}")

def print_stats(processes, algorithm_name):
    n = len(processes)
    total_waiting = sum(p.waiting_time for p in processes)
    total_turnaround = sum(p.turnaround_time for p in processes)
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n
    throughput = n / max(p.completion_time for p in processes)
    print(f"\nStats for {algorithm_name}:")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Throughput: {throughput:.2f} processes/unit time")


def main():
    processes = [
        Process(pid=1, burst_time=6, priority=2, arrival_time=1),
        Process(pid=2, burst_time=8, priority=1, arrival_time=1),
        Process(pid=3, burst_time=7, priority=3, arrival_time=2),
        Process(pid=4, burst_time=3, priority=2, arrival_time=3),
    ]

    #  FCFS
    fcfs_result = fcfs_scheduling(processes.copy())
    print_results(fcfs_result, "FCFS")
    print_stats(fcfs_result, "FCFS")

    #  SJF
    sjf_result = sjf_scheduling(processes.copy())
    print_results(sjf_result, "SJF")
    print_stats(sjf_result, "SJF")

    #  Priority
    priority_result = priority_scheduling(processes.copy())
    print_results(priority_result, "Priority")
    print_stats(priority_result, "Priority")
    
    # SRTF
    srtf_result = srtf_scheduling(processes.copy())
    print_results(srtf_result, "SRTF")
    print_stats(srtf_result, "SRTF")

    #Preemptive Priority
    preemptive_priority_result = preemptive_priority_scheduling(processes.copy())
    print_results(preemptive_priority_result, "Preemptive Priority")
    print_stats(preemptive_priority_result, "Preemptive Priority")

    #Round Robbin
    rr_result = round_robin_scheduling(processes.copy(), time_quantum=2)
    print_results(rr_results, "Round Robin")
    print_stats(rr_result, "Round Robin")


if __name__ == "__main__":
    main()







