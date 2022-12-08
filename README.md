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
    - A process is said to be running if it currently has the CPU
    - A process is said to be ready if it could use the CPU if one were available
    - A process is said to be blocked if it is waiting for some event to happen before it can proceed
* Non-preemptive - _Process CAN'T be taken away by another process_
    * First Come First Serve
    * Shortest Job First
    * Priority
* Preemptive - _Process CAN be taken away by another process_
    * Priority
    * Shortest Remaining Time First
    * Round Robin
        > Quantum time = 5

### Screenshots
![menu_screen](https://user-images.githubusercontent.com/67821138/149616923-b6fb6d4b-0e9f-4dd6-95be-b2a820e07cf0.png)
![menu_screen_dark](https://user-images.githubusercontent.com/67821138/149616928-719530f0-bebb-4c7b-8536-f521c3de14fb.png)
![single_con_input](https://user-images.githubusercontent.com/67821138/149616939-abdc660b-b484-409c-9099-bc7249e4b81f.png)
![single_con_sim](https://user-images.githubusercontent.com/67821138/149616943-f292d7a4-1fd1-4589-8077-2c79187e63e4.png)
![single_con_sim_summary](https://user-images.githubusercontent.com/67821138/149616944-0bee973b-9039-4da7-893f-e7212cdecb27.png)
![dynamic_inpWindow](https://user-images.githubusercontent.com/67821138/149616948-f9f10831-ce57-40d2-b6dd-ef204d113d7a.png)
![dynamic_simWindow](https://user-images.githubusercontent.com/67821138/149616952-980f0652-150a-497b-8b50-9dd3332b3581.png)
![dynamic_simWindowb](https://user-images.githubusercontent.com/67821138/149616958-fd60edd8-322f-4d2a-ba28-36b1d523390d.png)
![process_inpWindow](https://user-images.githubusercontent.com/67821138/149616960-8ed4267c-1998-4228-83b7-787ce6828c5c.png)
![process_simWindow](https://user-images.githubusercontent.com/67821138/149616964-639b0e32-d6fc-461d-b35b-39007d1cb7db.png)

### UI used
* PyQt5
