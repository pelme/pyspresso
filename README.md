# pyspresso

A project to build a PID controlled Gaggia Classic with a Raspberry Pi, using
Python.

## Installation and configuration

* Install Raspbian Wheezy Lite on a memory card
* Use raspi-config to set
  * Interfacing options/SSH: Enable (not neccessary but useful)
  * Interfacing options/I2C: Enable
  * Boot options/Wait for network at boot: Disable (gives faster boot time)
* Clone this repo in /root/pyspresso
* Install everything:
```
apt-get install python3.4 libffi-dev pigpio virtualenv

virtualenv -p python3.4 /pyspresso-venv

source /pyspresso-venv/bin/activate

cd ~/pyspresso

pip install -e .

cat <<EOF > /etc/systemd/system/pyspressod.service
[Unit]
Description=pyspressod

[Service]
ExecStart=/pyspresso-venv/bin/pyspressod

[Install]
WantedBy=multi-user.target
EOF

systemctl enable pyspressod
systemctl start pyspressod
```
