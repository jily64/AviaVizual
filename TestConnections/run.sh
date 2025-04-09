#!/bin/bash
. .venv/bin/activate
mavproxy.py --out=udp:127.0.0.1:14550
deactivate