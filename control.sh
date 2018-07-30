#!/bin/bash

cd /root/python
python ./get_grades.py
d="`diff ./grades.csv ./grades_old.csv`"
if [ -z "$d" ];then  # 成绩未更新
        mv ./grades.csv ./grades_old.csv
else
        python ./send_mail.py
        sleep 5
        mv ./grades.csv ./grades_old.csv
fi