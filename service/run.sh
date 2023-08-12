#!/bin/bash
PROJECT_LXP="${PD_ROOT_DIRECTORY}/pleasure_dairy/lighting/scene_models/test-ring.lxp"

echo LXStudio run loop starting
java -jar "${PD_LXSTUDIO_JAR}" --headless "${PROJECT_LXP}"
echo LXStudio run loop exiting
