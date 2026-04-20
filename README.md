INSTALL:

cd ~/git/serial && python3 -m venv venv && source venv/bin/activate

pip install pyserial

LAUNCH:
cd ~/git/serial && source venv/bin/activate && sudo python main.py