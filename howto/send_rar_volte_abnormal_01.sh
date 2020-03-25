#!/bin/bash

./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --destination-host   csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --charging-rule-name  2 &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 2002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 2002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1 
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --supported-features    10415 1 2 &&
./minidclisender 172.21.21.241 4868 --supported-features      10415 2 128 &&
./minidclisender 172.21.21.241 4868 --destination-host  csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --remove-level-charging-rule-name 2 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
