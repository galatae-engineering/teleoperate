INSTALL:

cd ~/git/teleoperate && python3 -m venv venv && source venv/bin/activate
pip install pyserial
pip install opencv-python

LAUNCH:
cd ~/git/teleoperate && source venv/bin/activate && python main.py
ssh galatae@192.168.0.110