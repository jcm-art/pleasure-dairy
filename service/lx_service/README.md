# Setup Pi
The commands in `setupPi.sh` can be used to install dependencies after installing the 64-bit RPi OS Lite version on an SD card.

# Installing the service
The "service" folder contains `pdhost.service` and `installService.sh`. 
The service assumes the user is named 'cow', so this will need to be updated if the user is different. 

Once installed the service will call the script `/home/cow/git/pleasure-dairy/service/startupLoop.sh` after the Pi boots (takes ~20 seconds)

# Service overview
The script `startupLoop.sh` syncs changes from git, kills any running LXStudio instances, and then calls the script `run.sh` which starts a headless version of LX with a project file as input. 


