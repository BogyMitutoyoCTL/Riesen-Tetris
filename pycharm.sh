#!/bin/bash

# Make Java compatible with PyCharm
if [ "`java -version 2>&1 | grep version | grep 1.8.0_65 | wc -l`" -eq "1" ]; then
    echo -e "\e[91mJava is problematic Oracle version 1.8.0.65.\e[39m"
    echo -e "\e[96mSwitching to OpenJDK Ice-T version.\e[39m"
    apt-get purge -y oracle*
    apt-get update
    apt-get upgrade
    apt-get remove -y oracle*
    apt-get install -y openjdk-8-jre
    if [ "`java -version 2>&1 | grep version | grep 1.8.0_65 | wc -l`" -eq "0" ]; then
        echo -e "\e[92mJava update seems good.\e[39m"
    else
        echo -e "\e[91mJava is still 1.8.0_65.\e[39m"
        echo -e "\e[96mDo you have an active Internet connection?\e[39m"
        exit 3
    fi
else
    echo -e "\e[92mJava is not the broken version 1.8.0.65.\e[39m";
fi

if [ "`cat /etc/java-8-openjdk/accessibility.properties | grep ^assistive_technologies | wc -l`" -eq "1" ]; then
    # Back up config file
    cp /etc/java-8-openjdk/accessibility.properties /etc/java-8-openjdk/accessibility.properties$(date +%Y%m%d)
    sed -i -e "s/^assistive_technologies/#assistive_technologies/g" /etc/java-8-openjdk/accessibility.properties
fi

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
    cat <<-EOF > ~/.local/share/applications/pycharm.desktop
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
