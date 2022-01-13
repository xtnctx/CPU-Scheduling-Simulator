# CPU Scheduling Simulator

## Single Contiguous Memory Management
    One process at a time
  
## Partitioned Allocation Memory Management
    Main memory is divided into separate memory regions or memory partitions. Each holds a separate jobs address space.
* Static Partition - _Job sizes will enter the partition_
* Dynamic Partition - _Job sizes will enter the CPU to create a partition_
    * Best Fit
        > Allocate the smallest hole that is big enough
    * First Fit
        > Allocate the first hole that is big enough
## Process Management
    -- A process is said to be running if it currently has the CPU
    -- A process is said to be ready if it could use the CPU if one were available
    -- A process is said to be blocked if it is waiting for some event to happen before it can proceed
* Non-preemptive - _Process CAN'T be taken away by another process_
    * First Come First Serve
    * Shortest Job First
    * Priority
* Preemptive - _Process CAN be taken away by another process_
    * Priority
    * Shortest Remaining Time First
    * Round Robin
        > Quantum time = 5

### UI used
* PyQt5


_If an error showed, please message me at my FB account. [Ryan Christopher Bahillo](https://www.facebook.com/xtnctx)_
