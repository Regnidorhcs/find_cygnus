#!/usr/bin/env bash
python resetToZero.py
sleep 5
python resetToZero.py
sleep 5
python resetToZero.py

#python testScript.py
sleep 5
while true; do
   python findCygnus.py
   sleep 300
done

#sudo shutdown -h now
