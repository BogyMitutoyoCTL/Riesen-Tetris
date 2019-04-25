#!/bin/bash

# Download
wget https://download.jetbrains.com/python/pycharm-community-2019.1.1.tar.gz ~/

# Unpack
tar -xzf ~/pycharm-community-2019.1.1.tar.gz
mv ~/pycharm-community-2019.1.1 ~/pycharm

# Remove downloaded file
rm ~/pycharm-community-2019.1.1.tar.gz

# Create menu entry
if [ -e ~/.local/share/applications/pycharm.desktop ]; then
    echo "Pycharm menu entry already exists"
else
    echo <<-EOF > ~/.local/share/applications/pycharm.desktop
[Desktop Entry]
Comment=PyCharm
Terminal=false
Name=PyCharm
Exec=sudo /home/pi/pycharm/bin/pycharm.sh
Type=Application
Icon=/home/pi/pycharm/bin/pycharm.png
EOF

    if [ -e ~/.local/share/applications/alacarte-made.desktop ]; then
        number=1
        while [ -e "~/.local/share/applications/alacarte-made-$number.desktop" ]; do
            $((++number))
        done
        cp ~/.local/share/applications/pycharm.desktop ~/.local/share/applications/alacarte-made-$number.desktop
    else
        cp ~/.local/share/applications/pycharm.desktop ~/.local/share/applications/alacarte-made.desktop
    fi
fi

lxpanelctl restart

# Install
sudo ~/pycharm/bin/pycharm.sh
