#!/bin/bash

echo "FontAwesome donwload..."
wget http://use.fontawesome.com/releases/v5.8.1/fontawesome-free-5.8.1-web.zip -O fontawesome-free-web.zip
echo "Unzip Fontawesome"
unzip fontawesome-free-web.zip -d ./static/
echo "Remove downloaded zip file..."
mv ./static/fontawesome-free-5.8.1-web ./static/fontawesome-free-web
rm fontawesome-free-web.zip
echo "return to main folder.."
cd ..
echo "Done!"

