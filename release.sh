#!/bin/sh

mkdir -p tmp/usr/share/wificar
cp *py tmp/usr/share/wificar
cp -R www tmp/usr/share/wificar

mkdir -p tmp/lib/systemd/system
cp wificar.service tmp/lib/systemd/system

cp -R DEBIAN tmp

dpkg-deb -b tmp
mv tmp.deb wificar.ipk
rm -rf tmp

