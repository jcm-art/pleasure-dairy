#!/bin/bash
export PD_ROOT_DIRECTORY="${HOME}/git/pleasure-dairy"
export HOST_NAME=$(hostname)
export PD_LXSTUDIO_JAR="${PD_ROOT_DIRECTORY}/pleasure_dairy/lighting/LXStudio.jar"

# Auto-update code from git
ping -c 1 github.com> /dev/null 2>&1
returnCode=$?
if [[ $returnCode -eq 0 ]]; then
  git -C "${PD_ROOT_DIRECTORY}" pull
else
  echo aborting git pull, host unreachable
fi

while true; do
  # Check for zombie LXStudio.jar processes and kill them here
  "${PD_ROOT_DIRECTORY}/service/cleanLXStudioProcesses.sh"
  "${PD_ROOT_DIRECTORY}/service/run.sh"
  "${PD_ROOT_DIRECTORY}/service/startupLoop.sh" && exit
done
