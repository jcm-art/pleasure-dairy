#!/bin/bash
PIDS=$(ps aux | grep LXStudio.jar | grep -v grep | awk '{print $2}')
while read PID; do
  if [[ ! -z "${PID}" ]]; then
    echo killing zombie LXStudio.jar process with PID "${PID}"
    kill -9 "${PID}"
  fi
done <<< "$PIDS"
