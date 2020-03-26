#!/bin/bash

kill $(ps aux|grep $1|grep -v grep|grep -v $0|awk '{print $2}')
nohup ../minidiameterd -f $1 >/dev/null 2>/dev/null &
