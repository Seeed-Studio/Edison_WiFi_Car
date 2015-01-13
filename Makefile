#!/bin/sh


wificar.ipk:
	mkdir -p tmp/usr/share/wificar
	cp *py tmp/usr/share/wificar
	cp -R www tmp/usr/share/wificar

	mkdir -p tmp/lib/systemd/system
	cp wificar.service tmp/lib/systemd/system

	cd DEBIAN; tar czvf ../control.tar.gz control; cd ..
	cd tmp; tar czvf ../data.tar.gz .; cd ..
	echo 2.0 > debian-binary
	ar r wificar.ipk control.tar.gz data.tar.gz debian-binary

clean:
	rm -rf tmp
	rm -f control.tar.gz
	rm -f data.tar.gz
	rm -f debian-binary
	rm -f wificar.ipk

.PHONY: clean
