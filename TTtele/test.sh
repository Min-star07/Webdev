#!/bin/bash
#Simple for loop example
for i in {4..4}
do
    echo "Iteration: $i"
    #   ./RunFitter -led ./data/led_cCB-22_2023-12-18_18_12_hist.root -ped ./data/ped_cCB-22_2023-12-18_18_19_hist.root -ROB $i -channel_start 27 -channel_end 29  -sigma 3
    ./RunFitter -led ./data/led_cCB-19_2023-11-10_10_50_hist.root -ped ./data/ped_cCB-19_2023-11-10_10_49_hist.root -ROB $i -channel_start 0 -channel_end 64  -sigma 3
done
