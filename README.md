INSTALL:

cd ~/git/teleoperate && python3 -m venv venv && source venv/bin/activate
pip install pyserial
pip install opencv-python

LAUNCH:
cd ~/git/serial && source venv/bin/activate && sudo python main.py