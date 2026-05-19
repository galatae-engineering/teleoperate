cd ~/git/teleoperate && python3 -m venv venv && source venv/bin/activate
python -m pip install "kivy[base]" kivy_examples
pip install opencv-python
pip install RPi.GPIO

cd ~/git/teleoperate && source venv/bin/activate && python main.py