#!/bin/bash


case $1 in

va_01) 
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
;;

va_02)
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
./minidclisender 172.21.21.241 4868 --destination-host   csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --charging-rule-name  2 &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

va_03)
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
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

va_04)
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
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 3002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 3002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

va_05)
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
./minidclisender 172.21.21.241 4868 --destination-host   csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --charging-rule-name  3 && 
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 3002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 3002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 && 
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" && 
./minidclisender 172.21.21.241 4868 --rating-grp  60 && 
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

# CBR
va_06_1)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#UBR
va_06_2)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
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
;;


#CBR
va_07_1)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;


#UBR
va_07_2)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_08_1)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#UBR
va_08_2)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 59000 59000 59000 59000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_09_1)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#UBR
va_09_2)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 5222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 5222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_10_1)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#UBR
va_10_2)
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
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 3222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 3222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 4222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 4222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --destination-host   csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --charging-rule-name  3 && 
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 6002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 6002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 && 
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" && 
./minidclisender 172.21.21.241 4868 --rating-grp  60 && 
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_11_1)
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
;;

#DBR
va_11_2)
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --supported-features    10415 1 2 &&
./minidclisender 172.21.21.241 4868 --supported-features      10415 2 128 &&
./minidclisender 172.21.21.241 4868 --destination-host  csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --remove-level-charging-rule-name 2 &&
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
;;

#CBR
va_12_1)
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
;;

#DBR
va_12_2)
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --supported-features    10415 1 2 &&
./minidclisender 172.21.21.241 4868 --supported-features      10415 2 128 &&
./minidclisender 172.21.21.241 4868 --destination-host  csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --remove-level-charging-rule-name 2 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --destination-host   csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --charging-rule-name  2 && 
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 1002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 1002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 && 
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" && 
./minidclisender 172.21.21.241 4868 --rating-grp  60 && 
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --enable-online 0 &&
./minidclisender 172.21.21.241 4868 --enable-offline 1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_13_1)
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
;;

#DBR
va_13_2)
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --supported-features    10415 1 2 &&
./minidclisender 172.21.21.241 4868 --supported-features      10415 2 128 &&
./minidclisender 172.21.21.241 4868 --destination-host  csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --remove-level-charging-rule-name 2 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1 
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
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 49000 49000 49000 49000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_14_1)
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
;;

#DBR
va_14_2)
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --supported-features    10415 1 2 &&
./minidclisender 172.21.21.241 4868 --supported-features      10415 2 128 &&
./minidclisender 172.21.21.241 4868 --destination-host  csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --remove-level-charging-rule-name 2 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1 
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
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 3002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 3002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 &&
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" &&
./minidclisender 172.21.21.241 4868 --rating-grp  60 &&
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

#CBR
va_15_1)
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
;;

#DBR
va_15_2)
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --supported-features    10415 1 2 &&
./minidclisender 172.21.21.241 4868 --supported-features      10415 2 128 &&
./minidclisender 172.21.21.241 4868 --destination-host  csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --remove-level-charging-rule-name 2 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
sleep 1
./minidclisender 172.21.21.241 4868 --reset-rar-info-gx &&
./minidclisender 172.21.21.241 4868 --gx-command 3 &&
./minidclisender 172.21.21.241 4868 --destination-host   csc-nsa-smf-7 &&
./minidclisender 172.21.21.241 4868 --destination-realm kt.com &&
./minidclisender 172.21.21.241 4868 --charging-rule-name  3 && 
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit in ip from 3002:ac64:6130:24:0:19:ede0:f901 to 2222:2222:2222:2222::25"  &&
./minidclisender 172.21.21.241 4868 --flow-information   &&
./minidclisender 172.21.21.241 4868 --flow-info-flow-description "permit out ip from 2222:2222:2222:2222::25  to 3002:ac64:6130:24:0:19:ede0:f901"  &&
./minidclisender 172.21.21.241 4868 --flow-status  2 && 
./minidclisender 172.21.21.241 4868 --precedence   0 &&
./minidclisender 172.21.21.241 4868 --flow-authorized-qos "1 39000 39000 39000 39000  -1 1 1 0" && 
./minidclisender 172.21.21.241 4868 --rating-grp  60 && 
./minidclisender 172.21.21.241 4868 --report-level  1 &&
./minidclisender 172.21.21.241 4868 --resource-allocation-notification  0 &&
./minidclisender 172.21.21.241 4868 --event-trigger  14 &&
./minidclisender 172.21.21.241 4868 --rar-time 1
;;

esac
