# Auto test


How to run

아래와 같이 테스트 시나리오를 yaml로 작성하여 파이썬 코드를 실행한다.

```
> python3 auto.py -f test/{testlist.yaml}
```

Example of test_list.yaml

test_list.yaml의 경우 테스트 항목 목록을 정의한다.
```
[root@localhost auto_test]# cat test/testlist.yaml 
---
# test list

name: Basic Test

test_list:
- basic_test1.yaml
...
```


Example of test_proc.yaml

test_proc.yaml은 각 테스트 항목의 세부 진행 방법을 정의한다.
```
[root@localhost auto_test]# cat test/basic_test1.yaml
---
# Test Procedure
test_description:
- name: basic_001

test_prepartion:
- host: cp_cli
  hostfile: cp1.yaml
- host: cp_mon
  hostfile: cp1.yaml
- host: up_cli
  hostfile: up8.yaml
- host: up_mon
  hostfile: up8.yaml
- host: sim_cli
  hostfile: saesim1.yaml
- host: gx_cli
  hostfile: gx1.yaml
- host: ping_cli
  hostfile: gx1.yaml

# proc_type: [ mon_pro | show_cli | sim_sli | gx_cli ]
test_procedure:
- proc_type: mon_pro
  wait: 3
  loop: 1
  host: cp_mon
  cmd: mon subs imsi 450081030101806
  option: +,+
- proc_type: mon_pro
  wait: 3
  loop: 1
  host: up_mon
  cmd: mon pro
  option: 49,B,Y,+,a
- proc_type: gx_cli
  wait: 3
  loop: 1
  host: gx_cli
  cmd: cd GX_inkwon; ./start_pcrf.sh gx-ims17.cfg
- proc_type: sim_cli
  wait: 10
  loop: 1
  host: sim_cli
  cmd: cd sae_sim; ipython -i scripts/7F_inkwon/5g_nsa_no_urlcc.py
- proc_type: show_cli
  wait: 3
  loop: 1
  host: cp_cli
  cmd: show subs imsi 450081030101806
- proc_type: show_cli
  wait: 3
  loop: 1
  host: up_cli
  cmd: show subs imsi 450081030101806
  more: True
- proc_type: ping_cli
  wait: 3
  loop: 1
  host: ping_cli
  cmd: ping6
  imsi: 450081030101806
  option: -c 100 -i 1 -s 100
- proc_type: show_cli
  wait: 1
  loop: 3
  host: up_cli
  cmd: show subs imsi 450081030101806
  more: True
- proc_type: sim_cli
  wait: 3
  loop: 1
  host: sim_cli
  cmd: mme.clearSub()
- proc_type: sim_ctl
  wait: 3
  loop: 1
  host: sim_cli
  cmd: d

...
```


