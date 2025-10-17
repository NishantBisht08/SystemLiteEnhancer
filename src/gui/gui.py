#python -m src.gui.gui.py
import tkinter as tk
from tkinter import ttk, messagebox

# Import your scheduling algorithm and Process class
from src.classical.process import Process
from src.classical.fcfs import fcfs_scheduling
from src.classical.sjf import sjf_scheduling
from src.classical.nonpreemtive_priority import priority_scheduling
from src.classical.srtf import srtf_scheduling
from src.classical.preemptive_priority import preemptive_priority_scheduling


#  Create the main window
root = tk.Tk()
root.title("Process Scheduler GUI")

# Maintain a list for processes
processes = []

#  Function to add a process
def add_process():
        
        pid = int(pid_entry.get())
        arrival = int(arrival_entry.get())
        burst = int(burst_entry.get())
        priority = int(priority_entry.get() or 0)  # Priority can be empty
        processes.append(Process(pid, burst, priority, arrival))
        # Clear entries after adding
        pid_entry.delete(0, tk.END)
        arrival_entry.delete(0, tk.END)
        burst_entry.delete(0, tk.END)
        priority_entry.delete(0, tk.END)
        messagebox.showinfo("Process Added", f"Added process ID {pid}")

# Function to run selected scheduling algorithm
def run_scheduler():
    if not processes:
        messagebox.showwarning("Error", "Add at least one process!")
        return
    algo = algo_var.get()
    if algo == "FCFS":
        result = fcfs_scheduling(processes.copy())
    elif algo == "SJF":
        result = sjf_scheduling(processes.copy())
    elif algo == "Priority":
        result = priority_scheduling(processes.copy())
    elif algo == "SRTF":
        result = srtf_scheduling(processes.copy())
    elif algo == "Preemptive Priority":
        result = preemptive_priority_scheduling(processes.copy())
    else:
        messagebox.showerror("Error", "Please select an algorithm!")
        return
    # Clear old rows in table
    for item in tree.get_children():
        tree.delete(item)
    # Fill new rows
    for p in result:
        tree.insert("", tk.END, values=[
            p.pid, p.arrival_time, p.burst_time, p.priority, p.waiting_time, p.turnaround_time
        ])


# Input fields for process details
input_frame = tk.Frame(root)
input_frame.pack(pady=8)

tk.Label(input_frame, text="PID").grid(row=0, column=0)
pid_entry = tk.Entry(input_frame, width=5)
pid_entry.grid(row=1, column=0)

tk.Label(input_frame, text="Arrival").grid(row=0, column=1)
arrival_entry = tk.Entry(input_frame, width=5)
arrival_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Burst").grid(row=0, column=2)
burst_entry = tk.Entry(input_frame, width=5)
burst_entry.grid(row=1, column=2)

tk.Label(input_frame, text="Priority").grid(row=0, column=3)
priority_entry = tk.Entry(input_frame, width=5)
priority_entry.grid(row=1, column=3)

add_btn = tk.Button(input_frame, text="Add Process", command=add_process)
add_btn.grid(row=1, column=4, padx=10)

# Choose scheduling algorithm using radio buttons
algo_var = tk.StringVar()
algo_frame = tk.Frame(root)
algo_frame.pack(pady=8)

tk.Label(algo_frame, text="Algorithm:").pack(side=tk.LEFT)
for name in ["FCFS", "SJF", "Priority", "SRTF", "Preemptive Priority"]:
    tk.Radiobutton(algo_frame, text=name, variable=algo_var, value=name).pack(side=tk.LEFT, padx=5)


run_btn = tk.Button(root, text="Run Scheduler", command=run_scheduler)
run_btn.pack(pady=8)

# Table to display results
cols = ["PID", "Arrival", "Burst", "Priority", "Waiting", "Turnaround"]
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=80)
tree.pack(pady=8)

# Start the main GUI event loop
root.mainloop()
