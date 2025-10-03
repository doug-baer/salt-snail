# salt-snail

This is a simple Salt setup for a quick demo environment that uses open source Salt and mostly defaults. 

There is one master: salt-master
There are two minions: salt-minion-01, salt-minion-02 (set with minion IDs of minion-01 and minion-02, respectively)

The demo user I use on my master and minions is "tech." 
I should probably stuff that into a pillar and pull that dynamically into the state files, but I haven't gotten there yet.

The snail.py program is intended to be run on the minions, ideally from a terminal sessionm and provide visual feedback that a "nasty" process is running on the machine (and slowing it down?). The idea for that part of the demo is showing that Salt can be used to search and destroy that process in short order across all minions or a subset of them. 

The reactor is a work in progress that responds to a minion connecting to the master and requests the minion to fire a connection to a webserver with a defined payload.

Note that the srv/salt/malware_demo/snail file is a python compiled binary that was created from the snail.py file with the following command
`pyinstaller --onefile --name snail snail.py`

To get my dev environment setup for the comopilation, I used a venv since Ubuntu didn't want me to break it with random python packages loaded into to the base:
```
sudo apt install python3.12-venv
python3 -m venv .venv && source .venv/bin/activate
pip install asciimatics
pip install pyinstaller
```

-Doug Baer October 2, 2025