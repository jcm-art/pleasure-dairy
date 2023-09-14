#!/bin/bash
ROOT_DIRECTORY="${HOME}/git/pleasure-dairy"
echo 'Copying service config to filesystem'
sudo cp "${ROOT_DIRECTORY}/service/pdhost.service" /etc/systemd/system/

echo 'installing pdhost.service'
sudo systemctl enable pdhost.service
