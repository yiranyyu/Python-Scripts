#!/usr/bin/python3
import subprocess
import time
import os
import sys
from datetime import datetime
from typing import List


def flush(*args, **kargs):
    print(*args, **kargs, flush=True)


args: List[str] = sys.argv[1:]
if not args or '-h' in args:
    flush('''Usage:
      trace_cpu <process_name>''')
    exit(1)

name = args[0]
gap = 2
flush('time user pid cpu command')
while True:
    result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
    result = subprocess.run(
        ['grep', name], input=result.stdout, stdout=subprocess.PIPE)

    data = result.stdout.decode('utf8').strip().split()
    if not data:
        flush(f'No data collected for process {name}')
        exit(1)
    user, pid, cpu, mem, *_, command = data
    now = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    flush(f'{now} {user} {pid} {cpu: <5} {command}')
    time.sleep(gap)
