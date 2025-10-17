#python -m src.CLI.cli_forschedule
from src.classical.process import Process
from src.classical.fcfs import fcfs_scheduling
from src.classical.sjf import sjf_scheduling
from src.classical.nonpreemtive_priority import priority_scheduling
from src.classical.srtf import srtf_scheduling
from src.classical.preemptive_priority import preemptive_priority_scheduling


def input_process():
    pid = int(input("Enter process ID: "))
    arrival = int(input("Enter arrival time: "))
    burst = int(input("Enter burst time: "))
    priority = int(input("Enter priority (default 0): ") or 0)
    return Process(pid, burst, priority, arrival)

def main():
    processes = []
    n = int(input("How many processes? "))
    for _ in range(n):
        processes.append(input_process())

    print("Select Algorithm: 1- FCFS, 2- SJF, 3- Priority, 4- SRTF, 5- Preemptive Priority")
    choice = input()

    if choice == '1':
        result = fcfs_scheduling(processes)
        algo_name = "FCFS"
    elif choice == '2':
        result = sjf_scheduling(processes)
        algo_name = "SJF"
    elif choice == '3':
        result = priority_scheduling(processes)
        algo_name = "Priority"
    elif choice == '4':
        result = srtf_scheduling(processes)
        algo_name = "SRTF"
    elif choice == '5':
        result = preemptive_priority_scheduling(processes)
        algo_name = "Preemptive Priority"        
    else:
        print("Invalid choice")
        return

    print(f"\nResults for {algo_name}:")
    print("PID\tArrival\tBurst\tPriority\tWaiting\tTurnaround")
    for p in result:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.priority}\t\t{p.waiting_time}\t{p.turnaround_time}")

if __name__ == "__main__":
    main()

