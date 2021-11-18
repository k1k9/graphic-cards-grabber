#!/usr/bin/env python3
import os

CURRENT = os.path.dirname(os.path.realpath(__file__))

# Creaing directory for log files
LOG_DIR = f"{CURRENT}/logs/"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# Creating sended urls "database"
if "sended_urls" not in os.listdir(CURRENT):
    with open("sended_urls", 'w') as f:
        pass

print("Setting up was successfully ended")
