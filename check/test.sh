#!/bin/bash
#Simple for loop example
for i in {15..15}
do
    echo "Iteration: $i"
    #  ./RunFitter -led ./data/led_cCB-22_2023-12-18_18_12_hist.root -ped ./data/ped_cCB-22_2023-12-18_18_19_hist.root -ROB $i -channel_start 27 -channel_end 29  -sigma 3
    ./RunFitter -led ../data/led_cCB-22_2023-12-18_18_18_hist.root -ped ../data/ped_cCB-22_2023-12-18_18_20_hist.root -ROB $i -channel_start 58 -channel_end 59  -sigma 3
done
