#!/bin/bash
PROJECT_LXP="${PD_ROOT_DIRECTORY}/pleasure_dairy/lighting/scratch_pad/test-ring.lxp"
PROJECT_LXP2="${PD_ROOT_DIRECTORY}/pleasure_dairy/lighting/scratch_pad/test-ring2.lxp"

echo LXStudio run loop starting
java -jar "${PD_LXSTUDIO_JAR}" --headless "${PROJECT_LXP}"
echo LXStudio run loop exiting
