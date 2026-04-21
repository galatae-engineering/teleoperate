INSTALL:

cd ~/git/teleoperate && python3 -m venv venv && source venv/bin/activate
pip install pyserial
pip install opencv-python
pip install keyboard

LAUNCH:
sudo ~/git/teleoperate/venv/bin/python main.py
ssh -X galatae@192.168.0.110