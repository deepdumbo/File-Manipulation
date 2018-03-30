#!/bin/bash

start=929
while [ $start -le 1429 ]
do
  end=$((start + 10))
  echo "Start:" $start "End:" $end
  python massConvertDicomToPng.py -s $start -e $end
  ((start += 10))
done
