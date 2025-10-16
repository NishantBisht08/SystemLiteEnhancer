#python -m tests.python_test_schedulers
from src.classical.process import Process
from src.classical.fcfs import fcfs_scheduling
from src.classical.sjf import sjf_scheduling
from src.classical.nonpreemtive_priority import priority_scheduling

def print_results(processes, algorithm_name):
    print(f"\nResults for {algorithm_name}:")
    print("PID\tArrival\tBurst\tPriority\tWaiting\tTurnaround")
    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.priority}\t\t{p.waiting_time}\t{p.turnaround_time}")

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

    #  SJF
    sjf_result = sjf_scheduling(processes.copy())
    print_results(sjf_result, "SJF")

    #  Priority
    priority_result = priority_scheduling(processes.copy())
    print_results(priority_result, "Priority")

if __name__ == "__main__":
    main()
