# input_fixed_30.py
from src.classical.process import Process

def get_fixed_30_processes():
    """
    Returns a list of 30 handcrafted Process objects for stress testing.
    This mix favors algorithms like MPP/DRR/DRR0—features tight batches,
    increasing burst, and priority variations.
    """
    return [
        Process(pid=1,  burst_time=2,  priority=2, arrival_time=0),
        Process(pid=2,  burst_time=3,  priority=3, arrival_time=0),
        Process(pid=3,  burst_time=1,  priority=1, arrival_time=0),
        Process(pid=4,  burst_time=2,  priority=2, arrival_time=1),
        Process(pid=5,  burst_time=5,  priority=3, arrival_time=1),
        Process(pid=6,  burst_time=7,  priority=2, arrival_time=2),
        Process(pid=7,  burst_time=4,  priority=1, arrival_time=2),
        Process(pid=8,  burst_time=3,  priority=1, arrival_time=3),
        Process(pid=9,  burst_time=8,  priority=4, arrival_time=3),
        Process(pid=10, burst_time=6,  priority=2, arrival_time=3),

        Process(pid=11, burst_time=10, priority=3, arrival_time=5),
        Process(pid=12, burst_time=2,  priority=1, arrival_time=5),
        Process(pid=13, burst_time=1,  priority=2, arrival_time=6),
        Process(pid=14, burst_time=7,  priority=4, arrival_time=6),
        Process(pid=15, burst_time=3,  priority=1, arrival_time=7),
        Process(pid=16, burst_time=2,  priority=1, arrival_time=8),
        Process(pid=17, burst_time=4,  priority=3, arrival_time=8),
        Process(pid=18, burst_time=5,  priority=2, arrival_time=9),
        Process(pid=19, burst_time=2,  priority=4, arrival_time=9),
        Process(pid=20, burst_time=6,  priority=1, arrival_time=10),

        Process(pid=21, burst_time=9,  priority=3, arrival_time=12),
        Process(pid=22, burst_time=8,  priority=2, arrival_time=12),
        Process(pid=23, burst_time=7,  priority=1, arrival_time=13),
        Process(pid=24, burst_time=5,  priority=4, arrival_time=13),
        Process(pid=25, burst_time=4,  priority=2, arrival_time=14),
        Process(pid=26, burst_time=2,  priority=1, arrival_time=14),
        Process(pid=27, burst_time=1,  priority=1, arrival_time=15),
        Process(pid=28, burst_time=2,  priority=3, arrival_time=16),
        Process(pid=29, burst_time=3,  priority=2, arrival_time=16),
        Process(pid=30, burst_time=5,  priority=1, arrival_time=17),
    ]
