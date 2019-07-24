''' CameraStreamer.py '''
print(" - CameraStreamer.py loaded")

### This library allows the python code to interface with the bash console of the operating system, giving more flexability to the program ###
import os

### This runs the existing camera streamer program in a 'screen' which allows it to run without having to keep the program running in the foreground, this helps to keep the asynchronicity of the program working correctly ###
CMD = "screen -dmS MJPG sh /opt/mjpg-streamer/mjpg-streamer-experimental/run.sh"
os.system(CMD)