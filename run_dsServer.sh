#!/bin/bash;
cd /home/pi/apps/dsServer;
/home/pi/apps/envs/dsenv/bin/python3 -m flask run --port 8100 --host 0.0.0.0;
